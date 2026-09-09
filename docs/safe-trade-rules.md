# Safe Trade Rules

## 목적

Trust404가 중고거래 과정에서 거래 조건이 안전거래 기준과
충돌하는지 판단하기 위한 기본 규칙을 정의한다.

본 규칙은 특정 거래를 사기라고 확정하기 위한 기준이 아니라,
거래 과정에서 추가 확인이 필요한 위험 상황을 탐지하기 위한 기준으로 사용한다.

---

## 안전거래 규칙

| Rule ID | 분류 | 안전거래 규칙 | 충돌 조건 | 관련 Risk |
|---|---|---|---|---|
| SAFE_PAYMENT_01 | 안전결제 | 가능한 경우 안전결제 방식을 우선한다. | 구매자가 안전결제를 제안했으나 판매자가 특별한 이유 없이 거부하고 계좌이체만 요구 | RISK_PAYMENT_REFUSAL |
| SAFE_PAYMENT_02 | 선입금 | 상품 및 거래 조건 확인 전 선입금을 요구하지 않는다. | 상품 확인 또는 거래 확정 전에 예약금·전체 금액 송금을 요구 | RISK_PREPAYMENT |
| SAFE_TRANSFER_01 | 계좌이체 | 계좌이체 전 판매자 및 거래 정보를 충분히 확인한다. | 충분한 확인 없이 즉시 계좌이체를 요구하거나 입금을 반복적으로 재촉 | RISK_PAYMENT_PRESSURE |
| SAFE_MEETUP_01 | 직거래 | 직거래로 합의한 경우 장소와 거래 방식을 임의로 변경하지 않는다. | 판매글에서는 직거래 가능이라고 했지만 채팅에서 특별한 이유 없이 택배만 요구 | RISK_MEETUP_AVOIDANCE, RISK_CONDITION_CHANGE |
| SAFE_PLATFORM_01 | 플랫폼 | 가능한 경우 거래 관련 대화를 플랫폼 내부에서 유지한다. | 거래 진행 중 외부 메신저로 이동하도록 지속적으로 요구 | RISK_EXTERNAL_MESSENGER |
| SAFE_VERIFY_01 | 상품 인증 | 구매자가 합리적인 상품 인증을 요청하면 확인 가능한 자료를 제공한다. | 추가 사진·인증 사진·영상 등을 특별한 이유 없이 거부 | RISK_VERIFICATION_REFUSAL |
| SAFE_CONDITION_01 | 거래조건 | 가격·배송·결제 방식 등 핵심 거래 조건을 명확하게 유지한다. | 거래 과정에서 핵심 조건이 반복적으로 변경됨 | RISK_CONDITION_CHANGE |
| SAFE_DESCRIPTION_01 | 상품정보 | 판매글과 채팅에서 상품 상태 및 구성에 대한 설명이 일관되어야 한다. | 판매글과 채팅의 상품 상태·구성 설명이 서로 다름 | RISK_DESCRIPTION_CONTRADICTION |
| SAFE_PRESSURE_01 | 거래 진행 | 구매자에게 비정상적으로 빠른 결정을 강요하지 않는다. | 시간 제한이나 다른 구매자를 이유로 즉시 입금을 반복적으로 요구 | RISK_PAYMENT_PRESSURE, RISK_URGENCY |
| SAFE_PRICE_01 | 가격 | 비정상적으로 낮은 가격인 경우 가격 사유와 상품 상태를 추가 확인한다. | 일반적인 거래 가격보다 현저히 낮은 가격과 즉시 입금 요구가 함께 나타남 | RISK_ABNORMAL_PRICE |

## 데이터 구조 예시

```json
[
  {
    "rule_id": "SAFE_PAYMENT_01",
    "category": "PAYMENT",
    "title": "안전결제 우선",
    "description": "가능한 경우 안전결제 방식을 우선한다.",
    "conflict_condition": "안전결제 제안 후 특별한 이유 없이 거부하고 계좌이체만 요구",
    "related_risks": [
      "RISK_PAYMENT_REFUSAL"
    ],
    "severity": "HIGH"
  },
  {
    "rule_id": "SAFE_VERIFY_01",
    "category": "VERIFICATION",
    "title": "상품 인증 확인",
    "description": "합리적인 상품 인증 요청에 확인 가능한 자료를 제공한다.",
    "conflict_condition": "추가 사진이나 인증 자료 제공을 특별한 이유 없이 거부",
    "related_risks": [
      "RISK_VERIFICATION_REFUSAL"
    ],
    "severity": "MEDIUM"
  }
]