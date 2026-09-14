from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.ai.risk_detection import RiskPattern, analyze_risk
from app.ai.consistency import Inconsistency, analyze_consistency
from app.services.risk_engine import RiskLevel, calculate_risk
from app.services.guidance import get_guidance_structure


app = FastAPI(
    title="Trust404 API",
    description="AI 기반 중고거래 사기 위험 분석 API",
    version="0.1.0",
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


class AnalyzeRequest(BaseModel):
    listing: str
    chat: str


class AnalyzeResponse(BaseModel):
    risk_score: int
    risk_level: RiskLevel
    patterns: list[RiskPattern]
    inconsistencies: list[Inconsistency]
    trade_stage: str
    summary: str
    checkpoints: list[str]


@app.get("/")
def root():
    return {"message": "Trust404 API"}


@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    try:
        risk_result = analyze_risk(
            listing=request.listing,
            chat=request.chat,
        )

        consistency_result = analyze_consistency(
            listing=request.listing,
            chat=request.chat,
        )

        risk_score, risk_level = calculate_risk(
            patterns=risk_result.patterns,
            inconsistencies=consistency_result.inconsistencies,
        )

        guidance = get_guidance_structure(
            consistency_result.trade_stage
        )

        return AnalyzeResponse(
            risk_score=risk_score,
            risk_level=risk_level,
            patterns=risk_result.patterns,
            inconsistencies=consistency_result.inconsistencies,
            trade_stage=consistency_result.trade_stage,
            summary=risk_result.summary,
            checkpoints=guidance["actions"],
        )

    except ValueError as error:
        raise HTTPException(
            status_code=400,
            detail=str(error),
        )

    except Exception as error:
        raise HTTPException(
            status_code=500,
            detail=f"분석 중 오류가 발생했습니다: {str(error)}",
        )