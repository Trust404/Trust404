# Consistency Evaluation - 2026-09-15

## Evaluation Dataset

- Total Cases: 43
- 기존 B001~B035에서 B036~B043까지 평가 데이터를 확대했다.
- 정상적인 가격 인하, 배송비 별도 안내, 배송 방식 구체화, 상품 상태 추가 설명 등 False Positive 경계 사례를 추가했다.
- 결제 예정, 결제 요청, 결제 완료, 실제 피해 발생 등 Trade Stage 경계 사례를 추가했다.

## Baseline Evaluation

신규 B036~B043에 대해 Prompt v2 개선 전 평가한 결과:

- Total Cases: 8
- PASS: 7
- FAIL: 1
- Overall Exact Match: 87.5%
- Trade Stage: 4/4 (100.0%)
- Evidence: 1/1 (100.0%)

### B036 - False Positive

- Expected: `[]`
- Actual: `PRICE_MISMATCH`
- False Positive: `PRICE_MISMATCH`
- Cause: 판매자가 판매글 가격보다 낮은 가격을 제안한 정상적인 가격 조정을 가격 불일치로 판단했다.
- Improvement: 단순한 가격 숫자 차이가 아니라 실제 거래 조건의 모순 여부를 판단하도록 가격 불일치 규칙을 보강했다.

## Consistency Prompt v2 Improvement

가격 불일치 판단에서 다음 규칙을 추가 또는 명확화했다.

1. 판매글과 채팅의 가격 숫자가 다르다는 이유만으로 `PRICE_MISMATCH`를 판단하지 않는다.
2. 구매자의 가격 제안과 판매자의 수락으로 이루어진 정상적인 가격 협상은 불일치로 판단하지 않는다.
3. 판매자가 판매글보다 낮은 가격을 제안하거나 할인하는 경우 정상적인 가격 조정으로 판단한다.
4. 배송비, 수수료 등 상품 가격과 구분되는 부대비용 안내만으로 가격 불일치를 판단하지 않는다.
5. 판매자가 판매글보다 높은 금액을 일방적으로 실제 판매 가격으로 확정하거나 기존 가격을 번복해 추가 금액을 요구하는 경우 가격 불일치로 판단한다.

## False Positive Re-evaluation

가격 관련 Prompt 개선 후 신규 B036~B043을 다시 평가했다.

- Total Cases: 8
- PASS: 8
- FAIL: 0
- Overall Exact Match: 100.0%
- Trade Stage: 4/4 (100.0%)

B036의 `PRICE_MISMATCH` False Positive가 제거되었으며 B037~B043에서도 새로운 오류가 발생하지 않았다.

## Trade Stage Failure Analysis

가격 Prompt 개선 후 B001~B043 전체 회귀 평가에서 B035의 Trade Stage 오류가 확인되었다.

### B035 - Trade Stage Error

- Expected Trade Stage: `UNKNOWN`
- Actual Trade Stage: `BEFORE_PAYMENT`
- Mismatch Types: `[]`
- Cause: 결제 여부에 대한 직접적인 근거가 없는 상태에서 거래 조건을 확인하고 있다는 사실만으로 결제 전 단계라고 추론했다.
- Improvement: 결제 또는 송금 여부에 대한 명확한 입력 근거가 없으면 `BEFORE_PAYMENT` 또는 `AFTER_PAYMENT`를 추측하지 않고 `UNKNOWN`을 사용하도록 Prompt를 보강했다.

Trade Stage 판단에서 다음 규칙을 추가 또는 명확화했다.

1. 결제 또는 송금 완료에 대한 명확한 근거가 있는 경우 `AFTER_PAYMENT`를 사용한다.
2. 아직 결제하지 않았거나 앞으로 결제할 예정이라는 명확한 근거가 있는 경우 `BEFORE_PAYMENT`를 사용한다.
3. 거래 조건을 논의하거나 확인하고 있다는 사실만으로 `BEFORE_PAYMENT`를 추론하지 않는다.
4. 결제 요청을 받았다는 사실만으로 결제 완료를 추론하지 않는다.
5. 결제 여부를 확인할 수 없는 경우 `UNKNOWN`을 사용한다.
6. `CONFIRMED_DAMAGE` 및 `SUSPECTED_FRAUD`의 기존 우선순위는 유지한다.

## Trade Stage Targeted Re-evaluation

Trade Stage 관련 B019, B020, B021, B022, B023, B031, B032, B033, B034, B035, B040, B041, B042, B043을 재평가했다.

- Total Cases: 14
- PASS: 14
- FAIL: 0
- Overall Exact Match: 100.0%
- Trade Stage: 14/14 (100.0%)
- Evidence: 2/2 (100.0%)

B035는 기대값인 `UNKNOWN`으로 정상 분류되었으며 기존 Trade Stage 사례에서도 회귀가 발생하지 않았다.

## Full Regression Evaluation

Prompt v2 개선 후 B001~B043 전체 회귀 테스트 결과:

- Total Cases: 43
- PASS: 43
- FAIL: 0
- Overall Exact Match: 100.0%
- Trade Stage: 14/14 (100.0%)
- Evidence: 21/21 (100.0%)

이번 실행에서는 모든 mismatch type, 평가 대상 Trade Stage, Evidence pair가 기대값과 일치했다.

LLM 기반 분석의 특성상 실행 간 출력 변동 가능성이 있으므로 해당 수치는 현재 평가 데이터셋에 대한 이번 회귀 실행 결과로 기록한다.

## Guidance Mapping v2

Trade Stage별 policy/response guidance를 보강했다.

- `BEFORE_PAYMENT`: 거래 조건 재확인 및 조건 변경 시 결제 보류
- `AFTER_PAYMENT`: 거래 증빙 보관, 진행 상태 확인, 추가 결제 요구 대응
- `SUSPECTED_FRAUD`: 추가 결제 중단, 거래 자료 보존, 확인되지 않은 거래 방식 진행 방지
- `CONFIRMED_DAMAGE`: 피해 증빙 보존, 피해 경위 정리, 공식 피해 대응 절차 준비
- `UNKNOWN`: 결제 여부, 상품 수령 여부, 사기 의심 또는 피해 정황 추가 확인

기존 `goal`, `actions`, `requires_official_source` 구조를 유지했으며 API 공통 응답 계약은 변경하지 않았다.

Guidance Mapping 검증 결과:

- `BEFORE_PAYMENT`: PASS / `requires_official_source=False`
- `AFTER_PAYMENT`: PASS / `requires_official_source=True`
- `SUSPECTED_FRAUD`: PASS / `requires_official_source=True`
- `CONFIRMED_DAMAGE`: PASS / `requires_official_source=True`
- `UNKNOWN`: PASS / `requires_official_source=False`
- 모든 Trade Stage에서 actions 3개 정상 반환

## Result

- B036~B043 평가 데이터 추가 완료
- Consistency Prompt v2 개선 완료
- 정상적인 가격 조정에 대한 False Positive 감소 확인
- Trade Stage 과도 추론 개선 완료
- Trade Stage targeted evaluation 14/14 통과
- 전체 B001~B043 회귀 평가 43/43 통과
- Evidence 21/21 통과
- Trade Stage별 policy/response Guidance 보강 및 검증 완료
- 공통 규격의 mismatch type, trade_stage enum 및 API 응답 계약은 변경하지 않음