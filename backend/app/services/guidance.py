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
        "actions": [
            "판매글과 채팅에서 안내한 거래 조건이 서로 일치하는지 다시 확인하세요.",
            "결제 방식, 가격, 배송 또는 직거래 조건이 갑자기 변경되지 않았는지 확인하세요.",
            "확인되지 않은 거래 조건이 있다면 결제 전에 판매자에게 다시 확인하세요.",
        ],
        "requires_official_source": False,
    },
    "AFTER_PAYMENT": {
        "goal": "결제 이후 거래 상태와 필요한 확인 사항을 정리한다.",
        "actions": [
            "결제 또는 송금 내역과 판매자와의 채팅 내용을 보관하세요.",
            "약속한 발송 또는 거래 일정과 현재 진행 상태를 확인하세요.",
            "결제 이후 거래 조건이 변경되었다면 변경된 내용과 관련 대화를 기록해 두세요.",
        ],
        "requires_official_source": True,
    },
    "SUSPECTED_FRAUD": {
        "goal": "사기 의심 상황에서 추가 피해를 줄이기 위한 확인 사항을 안내한다.",
        "actions": [
            "추가 결제나 송금을 진행하기 전에 거래 내용을 다시 확인하세요.",
            "판매글, 채팅 내용, 결제 요청 정보 등 거래 관련 자료를 보관하세요.",
            "확인되지 않은 링크나 새로운 결제 수단을 요구받았다면 즉시 진행하지 말고 확인하세요.",
        ],
        "requires_official_source": True,
    },
    "CONFIRMED_DAMAGE": {
        "goal": "실제 피해 발생 이후 필요한 자료를 정리하고 후속 대응을 준비한다.",
        "actions": [
            "판매글, 판매자와의 채팅, 결제 또는 송금 내역 등 거래 증빙을 보관하세요.",
            "피해 금액, 거래 시각, 연락 내역 등 피해 상황을 시간 순서대로 정리하세요.",
            "공식 신고 또는 피해 대응 절차에 필요한 자료를 준비하세요.",
        ],
        "requires_official_source": True,
    },
    "UNKNOWN": {
        "goal": "현재 거래 단계를 판단하기 위한 추가 확인 사항을 안내한다.",
        "actions": [
            "아직 결제 또는 송금을 했는지 확인하세요.",
            "상품을 실제로 받았는지 또는 약속한 거래가 완료되었는지 확인하세요.",
            "사기 의심이나 실제 피해로 판단할 수 있는 추가 상황이 있는지 확인하세요.",
        ],
        "requires_official_source": False,
    },
}


def get_guidance_structure(trade_stage: TradeStage) -> dict:
    return GUIDANCE_STRUCTURE[trade_stage]