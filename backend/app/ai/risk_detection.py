import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field

from app.ai.prompts.risk_prompt import (
    RISK_SYSTEM_PROMPT,
    build_risk_user_prompt,
)


# backend/.env 파일 불러오기
ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)


# -----------------------------
# A의 Structured Output 정의
# -----------------------------

class RiskPattern(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "SAFE_PAYMENT_REFUSAL",
        "PREPAYMENT_REQUEST",
        "PAYMENT_PRESSURE",
        "EXTERNAL_CONTACT",
        "BANK_TRANSFER_ONLY",
        "PERSONAL_INFO_REQUEST",
        "SUSPICIOUS_CONDITION",
    ]
    label: str
    evidence: str
    confidence: float = Field(ge=0.0, le=1.0)


class RiskAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    patterns: list[RiskPattern]
    summary: str


# -----------------------------
# OpenAI API 호출 함수
# -----------------------------

def analyze_risk(listing: str, chat: str) -> RiskAnalysis:
    if not listing.strip() and not chat.strip():
        raise ValueError("판매글과 채팅 내용이 모두 비어 있습니다.")

    model = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    client = OpenAI()

    response = client.responses.create(
        model=model,
        instructions=RISK_SYSTEM_PROMPT,
        input=build_risk_user_prompt(
            listing=listing,
            chat=chat,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "risk_analysis",
                "schema": RiskAnalysis.model_json_schema(),
                "strict": True,
            }
        },
    )

    return RiskAnalysis.model_validate_json(response.output_text)


# -----------------------------
# 임시 실행 테스트
# -----------------------------

if __name__ == "__main__":
    test_listing = """
    아이폰 15 Pro 판매합니다.
    안전결제 가능합니다.
    택배 가능합니다.
    """

    test_chat = """
    안전결제는 안 받아요.
    지금 바로 계좌로 입금하시면 오늘 보내드릴게요.
    """

    result = analyze_risk(
        listing=test_listing,
        chat=test_chat,
    )

    print(
        json.dumps(
            result.model_dump(),
            ensure_ascii=False,
            indent=2,
        )
    )