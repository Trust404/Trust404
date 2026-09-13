from typing import Literal


TradeStage = Literal[
    "BEFORE_PAYMENT",
    "AFTER_PAYMENT",
    "SUSPECTED_FRAUD",
    "CONFIRMED_DAMAGE",
    "UNKNOWN",
]


GUIDANCE_STRUCTURE = {
    "BEFORE_PAYMENT": {
        "goal": "거래 전 위험 요소를 다시 확인하고 안전한 거래 조건을 점검한다.",
        "requires_official_source": False,
    },
    "AFTER_PAYMENT": {
        "goal": "결제 이후 거래 상태와 필요한 확인 사항을 정리한다.",
        "requires_official_source": True,
    },
    "SUSPECTED_FRAUD": {
        "goal": "사기 의심 상황에서 필요한 대응 정보를 제공한다.",
        "requires_official_source": True,
    },
    "CONFIRMED_DAMAGE": {
        "goal": "실제 피해 발생 이후 필요한 대응 정보를 제공한다.",
        "requires_official_source": True,
    },
    "UNKNOWN": {
        "goal": "현재 거래 단계를 판단하기 위한 추가 확인 사항을 안내한다.",
        "requires_official_source": False,
    },
}


def get_guidance_structure(trade_stage: TradeStage) -> dict:
    return GUIDANCE_STRUCTURE[trade_stage]