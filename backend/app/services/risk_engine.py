from typing import Literal

from app.ai.consistency import Inconsistency
from app.ai.risk_detection import RiskPattern


RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]

TradeStage = Literal[
    "BEFORE_PAYMENT",
    "AFTER_PAYMENT",
    "SUSPECTED_FRAUD",
    "CONFIRMED_DAMAGE",
    "UNKNOWN",
]


RISK_PATTERN_WEIGHTS = {
    "SAFE_PAYMENT_REFUSAL": 25,
    "PREPAYMENT_REQUEST": 20,
    "BANK_TRANSFER_ONLY": 15,
    "PAYMENT_PRESSURE": 15,
    "EXTERNAL_CONTACT": 10,
    "PERSONAL_INFO_REQUEST": 20,
    "SUSPICIOUS_CONDITION": 15,
}


INCONSISTENCY_SCORE = 25


TRADE_STAGE_MIN_SCORE = {
    "BEFORE_PAYMENT": 0,
    "AFTER_PAYMENT": 30,
    "SUSPECTED_FRAUD": 60,
    "CONFIRMED_DAMAGE": 80,
    "UNKNOWN": 0,
}


def calculate_risk_score(
    patterns: list[RiskPattern],
    inconsistencies: list[Inconsistency],
    trade_stage: TradeStage,
) -> int:
    score = 0

    detected_pattern_types = {pattern.type for pattern in patterns}

    for pattern_type in detected_pattern_types:
        score += RISK_PATTERN_WEIGHTS.get(pattern_type, 0)

    if inconsistencies:
        score += INCONSISTENCY_SCORE

    # 거래 단계에 따른 최소 위험 점수 보장
    score = max(
        score,
        TRADE_STAGE_MIN_SCORE[trade_stage],
    )

    return min(score, 100)


def calculate_risk_level(risk_score: int) -> RiskLevel:
    if risk_score >= 60:
        return "HIGH"

    if risk_score >= 30:
        return "MEDIUM"

    return "LOW"


def calculate_risk(
    patterns: list[RiskPattern],
    inconsistencies: list[Inconsistency],
    trade_stage: TradeStage,
) -> tuple[int, RiskLevel]:
    risk_score = calculate_risk_score(
        patterns=patterns,
        inconsistencies=inconsistencies,
        trade_stage=trade_stage,
    )

    risk_level = calculate_risk_level(risk_score)

    return risk_score, risk_level