from typing import Literal

from app.ai.consistency import Inconsistency
from app.ai.risk_detection import RiskPattern


RiskLevel = Literal["LOW", "MEDIUM", "HIGH"]


RISK_PATTERN_WEIGHTS = {
    "SAFE_PAYMENT_REFUSAL": 25,
    "PREPAYMENT_REQUEST": 20,
    "PAYMENT_PRESSURE": 15,
    "EXTERNAL_CONTACT": 10,
    "PERSONAL_INFO_REQUEST": 20,
}


INCONSISTENCY_SCORE = 25


def calculate_risk_score(
    patterns: list[RiskPattern],
    inconsistencies: list[Inconsistency],
) -> int:
    score = 0

    detected_pattern_types = {pattern.type for pattern in patterns}

    for pattern_type in detected_pattern_types:
        score += RISK_PATTERN_WEIGHTS.get(pattern_type, 0)

    if inconsistencies:
        score += INCONSISTENCY_SCORE

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
) -> tuple[int, RiskLevel]:
    risk_score = calculate_risk_score(
        patterns=patterns,
        inconsistencies=inconsistencies,
    )

    risk_level = calculate_risk_level(risk_score)

    return risk_score, risk_level