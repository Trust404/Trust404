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
            "판매글과 채팅에서 안내한 결제 방식, 가격, 배송 또는 직거래 조건이 서로 일치하는지 다시 확인하세요.",
            "판매자가 기존 거래 조건을 갑자기 변경했다면 변경 이유를 확인하고 납득하기 전에는 결제를 진행하지 마세요.",
            "결제 전에 상품 상태, 최종 거래 금액, 결제 방식, 전달 방식을 판매자와 다시 확인하세요.",
        ],
        "requires_official_source": False,
    },
    "AFTER_PAYMENT": {
        "goal": "결제 이후 거래 진행 상태를 확인하고 문제가 발생할 경우에 대비해 증빙을 보관한다.",
        "actions": [
            "결제 또는 송금 내역과 판매글, 판매자와의 채팅 내용을 삭제하지 말고 보관하세요.",
            "약속한 발송일, 운송장 또는 직거래 일정 등 현재 거래 진행 상태를 확인하세요.",
            "결제 이후 추가 금액이나 새로운 거래 조건을 요구받았다면 바로 추가 결제하지 말고 변경 내용과 관련 대화를 기록하세요.",
        ],
        "requires_official_source": True,
    },
    "SUSPECTED_FRAUD": {
        "goal": "사기 의심 상황에서 거래 진행을 보류하고 추가 피해 가능성을 줄인다.",
        "actions": [
            "추가 결제나 송금은 중단하고 판매글과 기존 채팅에서 합의한 거래 조건을 다시 확인하세요.",
            "판매글, 채팅 내용, 계좌 또는 결제 요청 정보 등 현재까지의 거래 자료를 보관하세요.",
            "확인되지 않은 외부 링크, 새로운 결제 수단 또는 추가 송금을 요구받았다면 진행하지 말고 공식적인 확인 절차를 검토하세요.",
        ],
        "requires_official_source": True,
    },
    "CONFIRMED_DAMAGE": {
        "goal": "확인된 피해에 대한 증빙을 보존하고 공식적인 피해 대응을 준비한다.",
        "actions": [
            "판매글, 판매자 정보, 채팅, 결제 또는 송금 내역 등 거래 증빙을 삭제하지 말고 보관하세요.",
            "피해 금액, 송금 시각, 약속한 거래 내용, 연락 두절 시점 등 피해 경위를 시간 순서대로 정리하세요.",
            "정리한 증빙을 바탕으로 관련 기관 또는 이용한 거래·결제 서비스의 공식 신고 및 피해 대응 절차를 확인하세요.",
        ],
        "requires_official_source": True,
    },
    "UNKNOWN": {
        "goal": "현재 거래 단계를 판단하는 데 필요한 정보를 먼저 확인한다.",
        "actions": [
            "결제 또는 송금을 이미 완료했는지, 아직 결제 전인지 확인하세요.",
            "결제했다면 상품 수령 여부와 약속한 발송 또는 거래 일정이 지켜지고 있는지 확인하세요.",
            "판매자 연락 두절, 상품 미수령 또는 명확한 사기 의심 정황이 있는지 추가로 확인하세요.",
        ],
        "requires_official_source": False,
    },
}


def get_guidance_structure(trade_stage: TradeStage) -> dict:
    return GUIDANCE_STRUCTURE[trade_stage]