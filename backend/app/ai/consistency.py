import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from openai import OpenAI
from pydantic import BaseModel, ConfigDict

from app.ai.prompts.consistency_prompt import (
    CONSISTENCY_SYSTEM_PROMPT,
    build_consistency_user_prompt,
)


ENV_PATH = Path(__file__).resolve().parents[2] / ".env"
load_dotenv(ENV_PATH)


class Inconsistency(BaseModel):
    model_config = ConfigDict(extra="forbid")

    type: Literal[
        "PAYMENT_METHOD_MISMATCH",
        "PRICE_MISMATCH",
        "DELIVERY_METHOD_MISMATCH",
        "ITEM_CONDITION_MISMATCH",
        "DIRECT_TRADE_MISMATCH",
        "OTHER_CONDITION_MISMATCH",
    ]
    listing_evidence: str
    chat_evidence: str
    severity: Literal[
        "LOW",
        "MEDIUM",
        "HIGH",
    ]
    reason: str


class ConsistencyAnalysis(BaseModel):
    model_config = ConfigDict(extra="forbid")

    inconsistencies: list[Inconsistency]
    trade_stage: Literal[
        "BEFORE_PAYMENT",
        "AFTER_PAYMENT",
        "SUSPECTED_FRAUD",
        "CONFIRMED_DAMAGE",
        "UNKNOWN",
    ]


def analyze_consistency(listing: str, chat: str) -> ConsistencyAnalysis:
    if not listing.strip() and not chat.strip():
        raise ValueError("판매글과 채팅 내용이 모두 비어 있습니다.")

    model = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    client = OpenAI()

    response = client.responses.create(
        model=model,
        instructions=CONSISTENCY_SYSTEM_PROMPT,
        input=build_consistency_user_prompt(
            listing=listing,
            chat=chat,
        ),
        text={
            "format": {
                "type": "json_schema",
                "name": "consistency_analysis",
                "schema": ConsistencyAnalysis.model_json_schema(),
                "strict": True,
            }
        },
    )

    return ConsistencyAnalysis.model_validate_json(response.output_text)


if __name__ == "__main__":
    test_listing = """
    아이폰 15 Pro 판매합니다.
    가격은 100만원입니다.
    안전결제 가능합니다.
    택배 가능합니다.
    """

    test_chat = """
    안전결제는 안 받아요.
    계좌이체로 보내주세요.
    아직 입금 전입니다.
    """

    result = analyze_consistency(
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