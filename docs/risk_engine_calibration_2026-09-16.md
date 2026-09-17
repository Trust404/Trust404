# Risk Engine Calibration - 2026-09-16

## 1. 목표

9/16 공동작업으로 Risk Engine의 현재 가중치와 위험 등급 기준을 검증한다.

검증 항목:
- Risk Pattern 가중치
- Consistency 불일치 점수
- Trade Stage 최소 점수
- 정상 / 의심 / 고위험 거래 구분
- 실제 /analyze 통합 흐름

## 2. 현재 Risk Engine

Risk Pattern 가중치:
- SAFE_PAYMENT_REFUSAL: 25
- PREPAYMENT_REQUEST: 20
- BANK_TRANSFER_ONLY: 15
- PAYMENT_PRESSURE: 15
- EXTERNAL_CONTACT: 10
- PERSONAL_INFO_REQUEST: 20
- SUSPICIOUS_CONDITION: 15

Consistency:
- 하나 이상의 inconsistency가 존재하면 +25

Trade Stage 최소 점수:
- BEFORE_PAYMENT: 0
- AFTER_PAYMENT: 30
- SUSPECTED_FRAUD: 60
- CONFIRMED_DAMAGE: 80
- UNKNOWN: 0

Risk Level:
- 0~29: LOW
- 30~59: MEDIUM
- 60~100: HIGH

## 3. Risk Engine 단위 테스트

### NORMAL
- Pattern: 없음
- Inconsistency: 없음
- Stage: BEFORE_PAYMENT
- 결과: 0 / LOW

### SUSPICIOUS
- SAFE_PAYMENT_REFUSAL
- BANK_TRANSFER_ONLY
- 결과: 40 / MEDIUM

### HIGH_RISK
- SAFE_PAYMENT_REFUSAL
- PREPAYMENT_REQUEST
- PAYMENT_PRESSURE
- Inconsistency 존재
- Stage: SUSPECTED_FRAUD
- 결과: 85 / HIGH

결과:
- LOW / MEDIUM / HIGH 구간이 의도대로 분리됨

## 4. /analyze E2E 테스트

### 정상 거래
- risk_score: 0
- risk_level: LOW
- patterns: []
- inconsistencies: []
- trade_stage: BEFORE_PAYMENT

### 복합 위험 거래
- SAFE_PAYMENT_REFUSAL
- BANK_TRANSFER_ONLY
- PAYMENT_PRESSURE
- PAYMENT_METHOD_MISMATCH
- risk_score: 80
- risk_level: HIGH
- trade_stage: BEFORE_PAYMENT

### 피해 발생 거래
- PREPAYMENT_REQUEST
- inconsistencies: []
- trade_stage: CONFIRMED_DAMAGE
- risk_score: 80
- risk_level: HIGH

별도 보증금 요구를 상품 가격 변경으로 판단하지 않아
PRICE_MISMATCH false positive가 발생하지 않은 것도 확인했다.

## 5. 최종 판단

현재 Risk Engine은 대표 테스트에서 정상 / 의심 / 고위험 구간을 구분했다.

현재 평가 결과만으로 기존 가중치를 변경할 근거가 충분하지 않으므로
9/16 Calibration에서는 가중치를 유지한다.

Risk Engine 최종 점수는 LLM이 직접 생성하지 않고
탐지된 A/B 결과와 deterministic rule을 기반으로 계산한다.

9/17 기능 동결 이후에는 반복적으로 확인되는 치명적인 통합 문제가 없는 한
새로운 가중치나 핵심 Risk Engine 규칙을 추가하지 않는다.
