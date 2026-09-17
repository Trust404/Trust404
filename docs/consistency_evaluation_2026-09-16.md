\# Consistency AI Evaluation - 2026-09-16



\## 1. 작업 목표



9/16 B 개인 작업으로 Consistency Prompt v3를 검수하고,

최종 Evaluation을 수행하여 불일치 탐지와 거래 단계 분류의 안정성을 확인했다.



주요 목표:



\- Prompt v3 개선

\- 신규 경계 평가 데이터 추가

\- 정상 거래 False Positive 감소

\- trade\_stage 경계 판단 강화

\- 전체 Evaluation 최종 실행

\- 남은 FP/FN 및 LLM 출력 변동성 기록



\---



\## 2. 신규 Evaluation 데이터



기존 B001\~B043에 최종 경계 사례 B044\~B051 8개를 추가했다.



\### B044

판매글 가격의 오타를 정정하고 더 낮은 가격을 안내하는 정상 거래.



Expected:

\- inconsistencies: \[]



\### B045

판매자가 판매글보다 높은 실제 상품 가격을 일방적으로 요구.



Expected:

\- PRICE\_MISMATCH



\### B046

직거래 가능 지역을 더 구체적으로 안내하는 정상 거래.



Expected:

\- inconsistencies: \[]



\### B047

판매글에서는 직거래 가능이지만 채팅에서 직거래를 거부.



Expected:

\- DIRECT\_TRADE\_MISMATCH



\### B048

판매글에서는 정상 작동이라고 했지만 채팅에서 핵심 기능 고장을 안내.



Expected:

\- ITEM\_CONDITION\_MISMATCH



\### B049

판매자가 입금 여부를 질문하지만 실제 결제 여부를 판단할 수 없는 상황.



Expected:

\- inconsistencies: \[]

\- trade\_stage: UNKNOWN



\### B050

결제 완료 후 별도 추가 결제를 요구받아 사용자가 명시적으로 사기를 의심.



Expected:

\- inconsistencies: \[]

\- trade\_stage: SUSPECTED\_FRAUD



\### B051

결제 후 추가 입금 요구, 상품 미수령, 연락 두절 및 실제 피해가 확인된 상황.



Expected:

\- inconsistencies: \[]

\- trade\_stage: CONFIRMED\_DAMAGE



\---



\## 3. Prompt v2 신규 사례 Baseline



Prompt v2 상태에서 B044\~B051을 먼저 실행했다.



결과:



\- 전체: 8

\- PASS: 5

\- FAIL: 3

\- Overall Exact Match: 62.5%

\- Trade Stage: 2/3 (66.7%)

\- Evidence: 5/5 (100.0%)



실패:



\### B049



Expected:

\- trade\_stage: UNKNOWN



Actual:

\- trade\_stage: BEFORE\_PAYMENT



원인:

판매자가 입금 여부를 확인하는 질문을 실제 결제 상태에 대한 근거로 과도하게 해석했다.



\### B050



Expected:

\- inconsistencies: \[]

\- trade\_stage: SUSPECTED\_FRAUD



Actual:

\- PRICE\_MISMATCH

\- trade\_stage: SUSPECTED\_FRAUD



원인:

별도 추가 결제 요구를 상품 자체 가격의 변경으로 해석하여 PRICE\_MISMATCH가 발생했다.



\### B051



Expected:

\- inconsistencies: \[]

\- trade\_stage: CONFIRMED\_DAMAGE



Actual:

\- PRICE\_MISMATCH

\- trade\_stage: CONFIRMED\_DAMAGE



원인:

피해 상황에서 등장한 추가 입금 요구를 상품 가격 변경으로 해석했다.



\---



\## 4. Prompt v3 개선



\### 4.1 PRICE\_MISMATCH 경계 강화



다음 원칙을 추가했다.



\- 보증금, 인증비, 추가 입금 등 별도 금액 요구 자체는 상품 가격 변경으로 간주하지 않는다.

\- 상품 가격 자체의 번복 또는 인상이라는 명확한 근거가 있을 때만 PRICE\_MISMATCH를 반환한다.

\- 위험하거나 의심스러운 추가 금액 요구와 판매글/채팅 간 가격 불일치를 구분한다.



\### 4.2 결제 상태 질문과 실제 결제 상태 분리



다음 원칙을 추가했다.



\- 판매자가 입금 여부를 질문하거나 확인을 요청했다는 사실만으로 BEFORE\_PAYMENT 또는 AFTER\_PAYMENT를 판단하지 않는다.

\- 구매자의 실제 결제 상태가 명확하지 않다면 UNKNOWN을 사용한다.



\### 4.3 SUSPECTED\_FRAUD 우선순위 강화



다음 원칙을 명확히 했다.



\- 명시적인 사기 의심 표현이 존재하면 실제 피해가 확인되지 않은 한 SUSPECTED\_FRAUD를 우선한다.

\- 이미 결제를 완료했더라도 명시적인 사기 의심 표현이나 구체적인 사기 의심 정황이 있으면 단순 AFTER\_PAYMENT보다 SUSPECTED\_FRAUD를 우선한다.



\### 4.4 inconsistency 최상위 판단 원칙 강화



다음 원칙을 추가했다.



\- 판매글과 채팅 양쪽에 비교 가능한 동일 거래 조건이 존재해야 한다.

\- 해당 조건이 서로 직접적으로 모순될 때만 inconsistency를 반환한다.

\- 채팅에 새로운 요구나 위험 정황이 등장했다는 사실만으로 inconsistency를 생성하지 않는다.

\- 위험 패턴 탐지와 판매글/채팅 불일치 탐지의 역할을 분리한다.



\---



\## 5. 신규 사례 회귀 평가



Prompt v3 적용 후 B044\~B051을 재평가했다.



결과:



\- 전체: 8

\- PASS: 7

\- FAIL: 1

\- Overall Exact Match: 87.5%

\- Trade Stage: 3/3 (100.0%)

\- Evidence: 4/4 (100.0%)



B044\~B050은 모두 PASS했다.



B051에서는 trade\_stage는 CONFIRMED\_DAMAGE로 정확했지만,

추가 입금 표현을 PRICE\_MISMATCH로 분류하는 False Positive가 다시 관찰되었다.



\---



\## 6. B051 반복 실행



B051의 출력 안정성을 확인하기 위해 동일 케이스를 3회 반복 실행했다.



결과:



1회차:

\- FAIL

\- PRICE\_MISMATCH False Positive

\- trade\_stage: CONFIRMED\_DAMAGE



2회차:

\- PASS

\- inconsistencies: \[]

\- trade\_stage: CONFIRMED\_DAMAGE



3회차:

\- FAIL

\- OTHER\_CONDITION\_MISMATCH False Positive

\- trade\_stage: CONFIRMED\_DAMAGE



결론:



\- trade\_stage는 3/3 모두 CONFIRMED\_DAMAGE로 안정적으로 분류했다.

\- inconsistency 분류에서는 동일 입력에 대해 PASS / PRICE\_MISMATCH / OTHER\_CONDITION\_MISMATCH가 관찰되었다.

\- LLM 기반 분류 특성상 복합 피해 상황에서 비결정적인 출력 변동성이 존재함을 확인했다.

\- 특정 케이스에 대한 추가적인 Prompt 과적합을 피하기 위해 이후 규칙 추가를 중단하고 전체 회귀 평가를 진행했다.



\---



## 7. 최종 보완 및 회귀 평가

초기 전체 Evaluation 이후 실패 사례를 분석하여
Prompt v3의 분류 경계를 추가로 명확히 했다.

주요 보완 내용:

- 상품의 물리적 상태/기능과 구성품 포함 여부의 분류 기준을 분리했다.
- 구성품 포함 여부가 판매글과 채팅에서 모순되는 경우 OTHER_CONDITION_MISMATCH로 분류하도록 명확히 했다.
- 판매글에서 명시한 발송 일정이 채팅에서 일방적으로 변경되는 경우 OTHER_CONDITION_MISMATCH로 판단하도록 기준을 보완했다.
- 별도 추가 송금 요구와 상품 자체 가격 변경을 더 명확하게 분리했다.
- 판매글 가격의 오타 정정 또는 판매자에게 유리하지 않은 가격 인하는 정상적인 가격 정정/조정으로 처리하도록 PRICE_MISMATCH 기준을 보완했다.

초기 실패 사례 B017, B025, B029, B051을 대상으로 재평가한 결과:

- 전체: 4
- PASS: 4
- FAIL: 0
- Overall Exact Match: 100.0%
- Trade Stage: 1/1 (100.0%)
- Evidence: 3/3 (100.0%)

이후 가격, 배송, 상품 상태, 직거래, 추가 금액 관련 주요 기존 사례 15개를 대상으로 회귀 평가를 수행했다.

결과:

- 전체: 15
- PASS: 15
- FAIL: 0
- Overall Exact Match: 100.0%
- Trade Stage: 2/2 (100.0%)
- Evidence: 6/6 (100.0%)

따라서 해당 보완으로 인해 주요 기존 정상/불일치 사례가 깨지는 현상은 관찰되지 않았다.

---

## 8. 반복 실행을 통한 출력 변동성 확인

전체 회귀 과정에서 일부 경계 사례는 동일 Prompt와 동일 입력에서도 실행마다 결과가 달라지는 현상이 관찰되었다.

### B030

결제 방식, 가격, 배송 방식이 동시에 불일치하는 복합 사례.

반복 실행 결과:

- 1회차: FAIL
- 2회차: PASS
- 3회차: PASS

FAIL 실행에서는 배송 방식과 직거래 조건 사이의 분류 경계가 흔들렸다.

### B044

판매글 가격의 오타를 판매자가 정정하고 더 낮은 실제 가격을 안내하는 정상 거래.

가격 정정 규칙 보완 전 반복 실행 결과:

- 1회차: FAIL
- 2회차: FAIL
- 3회차: PASS

이후 가격 오타 정정 및 가격 인하 기준을 명확히 한 뒤 B044를 다시 3회 반복 실행했다.

결과:

- 1회차: PASS
- 2회차: PASS
- 3회차: PASS

### B049 / B051

B049와 B051 역시 이전 실행에서는 PASS한 기록이 있으나,
최종 전체 Evaluation에서는 각각 trade_stage와 inconsistency 결과가 다시 변동했다.

이를 통해 일부 경계 및 복합 거래 사례에서는
동일 Prompt와 동일 입력에서도 LLM 출력이 비결정적으로 변할 수 있음을 확인했다.

---

## 9. 최종 전체 Evaluation

최종 Prompt v3 상태에서 B001~B051 전체 51개를 다시 실행했다.

최종 단일 실행 결과:

- 전체: 51
- PASS: 49
- FAIL: 2
- Overall Exact Match: 96.1%
- Trade Stage: 16/17 (94.1%)
- Evidence: 25/25 (100.0%)

이 수치는 내부 Evaluation 데이터 51건에 대한 최종 단일 실행 결과이며,
실제 서비스 전체에 대한 일반적인 정확도를 의미하지 않는다.

---

## 10. 최종 실패 사례

### B049

Expected:

- inconsistencies: []
- trade_stage: UNKNOWN

Actual:

- inconsistencies: []
- trade_stage: BEFORE_PAYMENT

분석:

판매자가 입금 여부를 확인하는 상황에서 실제 결제 완료 여부가 명확하지 않음에도
BEFORE_PAYMENT로 분류되었다.

동일 Prompt의 이전 실행에서는 UNKNOWN으로 정상 분류된 기록이 있어
경계 상황에서 trade_stage 출력 변동성이 존재함을 확인했다.

### B051

Expected:

- inconsistencies: []
- trade_stage: CONFIRMED_DAMAGE

Actual:

- PRICE_MISMATCH
- trade_stage: CONFIRMED_DAMAGE

분석:

실제 피해 단계인 CONFIRMED_DAMAGE는 정확하게 유지했지만,
별도의 추가 입금 요구를 상품 가격 변경으로 해석하여 PRICE_MISMATCH False Positive가 발생했다.

B051은 이전 반복 및 전체 평가에서 PASS한 기록도 존재하므로
복합 피해 상황에서 inconsistency 분류의 출력 변동성이 확인되었다.

---

## 11. 최종 판단

Prompt v3에서는 다음 부분을 최종적으로 보완했다.

- 결제 여부 질문과 실제 결제 상태 구분
- 명시적 사기 의심 상황의 trade_stage 우선순위
- 별도 추가금 요구와 상품 가격 변경 구분
- 상품 상태와 구성품 조건의 분류 경계
- 발송 일정 변경에 대한 OTHER_CONDITION_MISMATCH 기준
- 가격 오타 정정 및 가격 인하 정상 거래 처리
- 위험 패턴과 판매글/채팅 불일치 역할 분리
- inconsistency 생성 기준 강화

최종 내부 Evaluation 51건의 단일 실행 결과:

- Overall Exact Match: 96.1%
- Trade Stage: 94.1%
- Evidence Validation: 100.0%

초기 전체 평가에서 실패했던 B017, B025, B029, B051에 대한 규칙을 보완했고,
해당 4개 대상 평가에서는 4/4 PASS를 확인했다.

또한 주요 회귀 사례 15개에서 15/15 PASS를 확인했으며,
B044 가격 정정 사례는 최종 보완 후 3회 반복 실행에서 3/3 PASS를 확인했다.

다만 전체 반복 평가 과정에서 B030, B044, B049, B051 등 일부 경계/복합 사례가
동일 입력에서도 실행에 따라 PASS/FAIL이 변하는 현상이 관찰되었다.

따라서 단일 Evaluation에서 51/51을 만들기 위해 케이스별 규칙을 계속 추가하는 것보다
Prompt 과적합 가능성을 줄이고 실제 서비스 통합 과정에서 반복적으로 재현되는 문제를 확인하는 방향을 선택했다.

Prompt v3는 현재 상태로 동결한다.

이후 통합 테스트에서는 정상 거래, 의심 거래, 고위험 거래 및 조건 불일치가 포함된
실사용 형태의 샘플 거래를 통해 전체 서비스 흐름에서의 동작을 추가 확인한다.

---

## 12. Common Spec 준수

이번 작업에서는 Common Spec의 출력 계약을 변경하지 않았다.

- inconsistency type enum 변경 없음
- severity enum 변경 없음
- trade_stage enum 변경 없음
- JSON field 변경 없음
- 신규 API response field 추가 없음
---

## 13. 신고이력 기능 GO / NO-GO 결정

9/16 기준 신고이력 자동 조회 기능의 적용 여부를 검토했다.

결정:

- 자동 신고이력 조회 API 연동: NO-GO
- 공식 신고이력 조회 페이지 안내 방식: 유지

사유:

- 개발 일정 내 서비스에 안정적으로 적용할 수 있는 공식 신고이력 조회 API가 확보되지 않은 상태에서는 자동 조회 기능을 추가하지 않는다.
- 검증되지 않은 비공식 API 또는 크롤링 방식은 사용하지 않는다.
- 신고이력 조회는 보조적인 확인 수단이며, Trust404의 핵심 기능인 현재 거래 과정의 위험 패턴 및 조건 불일치 분석과 분리한다.
- 사용자가 필요할 경우 공식 기관의 신고이력 조회 페이지를 직접 확인할 수 있도록 안내하는 방향으로 처리한다.

따라서 9/16 AI 기능 최종 완성 범위에서는 자동 신고이력 조회 기능을 제외하고,
공식 조회 경로 안내를 Production 단계에서 연결하는 것으로 결정한다.

