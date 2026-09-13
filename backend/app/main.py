from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from app.ai.risk_detection import RiskPattern, analyze_risk
from app.ai.consistency import Inconsistency, analyze_consistency


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
    patterns: list[RiskPattern]
    summary: str
    inconsistencies: list[Inconsistency]
    trade_stage: str


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

        return AnalyzeResponse(
            patterns=risk_result.patterns,
            summary=risk_result.summary,
            inconsistencies=consistency_result.inconsistencies,
            trade_stage=consistency_result.trade_stage,
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