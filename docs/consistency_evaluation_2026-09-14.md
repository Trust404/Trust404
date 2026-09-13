# Consistency Evaluation - 2026-09-14

## Evaluation Dataset

- Total Cases: 35
- 기존 B001~B023에서 B024~B035까지 평가 데이터를 확대했다.
- 정상 거래, 가격 협상, 복합 불일치, 거래 단계, Evidence 추출 등의 경계 사례를 추가했다.

## Baseline Evaluation

Prompt 개선 전 35개 전체 평가 결과:

- Total Cases: 35
- PASS: 32
- FAIL: 3
- Overall Exact Match: 91.4%
- Trade Stage Accuracy: 9/10 (90.0%)
- Evidence Pair Accuracy: 22/22 (100.0%)

평가 과정에서 B024와 B025의 기대값을 Prompt 및 공통 규격의 의미에 맞게 재검토했다.

- B024: 구매자 가격 제안을 판매자가 수락한 정상 협상 → Expected `[]`
- B025: 오늘 발송과 내일 발송의 명확한 조건 변경 → Expected `OTHER_CONDITION_MISMATCH`

## Failure Analysis

### B015 - Type Classification Error

- Expected: `DIRECT_TRADE_MISMATCH`
- Actual: `DELIVERY_METHOD_MISMATCH`
- False Positive: `DELIVERY_METHOD_MISMATCH`
- False Negative: `DIRECT_TRADE_MISMATCH`
- Cause: 직거래 가능 여부의 직접적인 모순을 배송 방식 불일치로 분류했다.
- Improvement: 직거래 가능 여부가 직접 모순되는 경우 `DIRECT_TRADE_MISMATCH`를 우선하도록 Prompt를 보강했다.

### B024 - False Positive

- Expected: `[]`
- Actual: `PRICE_MISMATCH`
- False Positive: `PRICE_MISMATCH`
- Cause: 구매자의 가격 제안을 판매자가 수락한 정상적인 가격 협상을 가격 불일치로 판단했다.
- Improvement: 구매자 제안과 판매자 수락으로 합의된 가격은 정상 협상으로 판단하도록 Prompt를 보강했다.

### B031 - Trade Stage Error

- Expected Trade Stage: `AFTER_PAYMENT`
- Actual Trade Stage: `SUSPECTED_FRAUD`
- Mismatch Type: `PRICE_MISMATCH` correctly detected.
- Cause: 결제 완료 후 추가 금액 요구만으로 `SUSPECTED_FRAUD`를 추론했다.
- Improvement: 명확한 사기 의심 표현 또는 정황이 없는 경우 추가 금액 요구만으로 `SUSPECTED_FRAUD`를 판단하지 않도록 Prompt를 보강했다.

## Prompt Improvement

다음 판단 규칙을 추가 또는 명확화했다.

1. 정상적인 가격 협상과 판매자의 일방적인 가격 변경을 구분한다.
2. 직거래 가능 여부가 직접 모순되는 경우 `DIRECT_TRADE_MISMATCH`를 우선한다.
3. 단순한 조건 변경 또는 추가 금액 요구만으로 `SUSPECTED_FRAUD`를 추론하지 않는다.
4. 기존 Evidence 추출 규칙과 공통 규격의 출력 구조는 유지한다.

## Targeted Re-evaluation

Prompt 개선 대상이었던 B015, B024, B031을 재평가했다.

- Total: 3
- PASS: 3
- FAIL: 0
- Overall Exact Match: 100.0%
- Trade Stage: 1/1 (100.0%)
- Evidence: 2/2 (100.0%)

## Full Regression Evaluation

Prompt 개선 후 B001~B035 전체 회귀 테스트 결과:

- Total Cases: 35
- PASS: 34
- FAIL: 1
- Overall Exact Match: 97.1%
- Trade Stage: 10/10 (100.0%)
- Evidence: 20/21 (95.2%)

B030의 mismatch type 3종은 모두 기대값과 일치했으나 Evidence pair 1건이 원문 검증을 통과하지 않아 FAIL 처리되었다.

## B030 Evidence Re-evaluation

B030을 단독으로 다시 평가한 결과:

- PASS: 1/1
- Overall Exact Match: 100.0%
- Evidence: 3/3 (100.0%)

직접 Structured Output을 확인했을 때도 세 inconsistency의 `listing_evidence`와 `chat_evidence`가 실제 입력 원문에 존재했다.

따라서 B030에서 관찰된 Evidence 실패는 재실행에서 재현되지 않았으며, LLM 출력의 일시적인 변동 가능성이 있는 사례로 기록한다.

## Result

- Evaluation 데이터 확대 완료
- 오탐/미탐 및 분류 오류 기록 완료
- 실패 사례 기반 Prompt 개선 완료
- Trade Stage 평가 10/10 확인
- Evidence 추출은 B030에서 1회 변동이 관찰되었으나 단독 재평가에서 3/3 통과
- 공통 규격의 mismatch type 및 trade_stage enum은 변경하지 않음