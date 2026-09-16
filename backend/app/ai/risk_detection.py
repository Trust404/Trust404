import json
import os
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
import openai
from openai import OpenAI
from pydantic import BaseModel, ConfigDict, Field, ValidationError

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

def filter_normal_direct_trade_contact(
    result: RiskAnalysis,
    listing: str,
    chat: str,
) -> RiskAnalysis:
    combined = f"{listing}\n{chat}"

    # 직거래 상황인지 확인
    is_direct_trade = "직거래" in combined

    # 직거래 만남을 위한 정상적인 연락 표현
    normal_contact_phrases = [
        "도착하시면 전화",
        "도착하면 전화",
        "도착 시 전화",
        "도착하시면 연락",
        "도착하면 연락",
        "도착 시 연락",
    ]

    has_normal_contact = any(
        phrase in combined
        for phrase in normal_contact_phrases
    )

    # 실제로 거래 대화를 외부 채널로 이동시키는 표현
    external_channel_markers = [
        "카카오톡",
        "카톡",
        "텔레그램",
        "오픈채팅",
        "라인으로",
        "디스코드",
        "문자로 이야기",
        "문자로 대화",
        "여기 말고",
    ]

    has_external_move = any(
        marker in combined
        for marker in external_channel_markers
    )

    # 직거래 + 도착 연락이고,
    # 명시적인 외부 채널 이동 표현이 없다면 EXTERNAL_CONTACT 제거
    if is_direct_trade and has_normal_contact and not has_external_move:
        filtered_patterns = [
            pattern
            for pattern in result.patterns
            if pattern.type != "EXTERNAL_CONTACT"
        ]

        # EXTERNAL_CONTACT가 실제로 제거된 경우에만 summary도 정리
        if len(filtered_patterns) != len(result.patterns):
            if not filtered_patterns:
                summary = "탐지된 위험 신호가 없습니다."
            else:
                labels = [
                    pattern.label
                    for pattern in filtered_patterns
                ]
                summary = (
                    "탐지된 위험 신호: "
                    + ", ".join(labels)
                )

            return RiskAnalysis(
                patterns=filtered_patterns,
                summary=summary,
            )

    return result


# -----------------------------
# OpenAI API 호출 함수
# -----------------------------

def analyze_risk(listing: str, chat: str) -> RiskAnalysis:
    if not listing.strip() and not chat.strip():
        raise ValueError("판매글과 채팅 내용이 모두 비어 있습니다.")

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        raise RuntimeError(
            "AI 분석 서비스 설정이 올바르지 않습니다."
        )

    model = os.getenv("OPENAI_MODEL", "gpt-5-nano")

    client = OpenAI(
        api_key=api_key,
        timeout=45.0,
        max_retries=1,
    )

    try:
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

        if not response.output_text:
            raise RuntimeError(
                "AI 분석 결과를 받지 못했습니다."
            )

        result = RiskAnalysis.model_validate_json(
            response.output_text
)

        return filter_normal_direct_trade_contact(
            result=result,
            listing=listing,
            chat=chat,
)

    except openai.APITimeoutError:
        raise RuntimeError(
            "AI 분석 요청 시간이 초과되었습니다. 잠시 후 다시 시도해주세요."
        )

    except openai.RateLimitError:
        raise RuntimeError(
            "AI 분석 요청이 많습니다. 잠시 후 다시 시도해주세요."
        )

    except openai.APIConnectionError:
        raise RuntimeError(
            "AI 분석 서버에 연결할 수 없습니다. 잠시 후 다시 시도해주세요."
        )

    except openai.APIStatusError:
        raise RuntimeError(
            "AI 분석 서비스에서 오류가 발생했습니다."
        )

    except ValidationError:
        raise RuntimeError(
            "AI 분석 결과 형식이 올바르지 않습니다."
        )


# -----------------------------
# 임시 실행 테스트
# -----------------------------

if __name__ == "__main__":
    test_listing = """
    키보드 판매합니다.
강남역 직거래 가능합니다.
    """

    test_chat = """
    강남역에서 직거래하죠.
여기 말고 카카오톡으로 이야기해요.
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