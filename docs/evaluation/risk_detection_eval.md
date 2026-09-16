## Prompt 버전 기록

### Prompt v1

초기 Risk Detection Prompt.

평가 결과:

- 전체 케이스: 10
- PASS: 7
- FAIL: 3
- Exact Match: 70.0%

주요 문제:

- RISK_001: Ground Truth에 `BANK_TRANSFER_ONLY` 누락
- RISK_005: `PAYMENT_PRESSURE` 상황을 `PREPAYMENT_REQUEST`까지 탐지
- RISK_010: `SUSPICIOUS_CONDITION` 중복 탐지

---

### Prompt v2

v1 평가 결과를 바탕으로 다음을 수정함.

- `PREPAYMENT_REQUEST` 판정 조건 구체화
- 단순 입금 재촉은 `PAYMENT_PRESSURE`로 분리
- `SUSPICIOUS_CONDITION`을 fallback 유형으로 제한
- RISK_001 Ground Truth 수정

재평가 결과:

- 전체 케이스: 10
- PASS: 9
- FAIL: 1
- Exact Match: 90.0%

남은 문제:

- RISK_005에서 `PREPAYMENT_REQUEST` 추가 탐지

> 참고: v1 → v2의 70% → 90% 변화는 Prompt 개선만의 효과가 아니다.
> RISK_001의 Ground Truth 수정도 포함되어 있으므로
> Prompt 성능 향상과 평가 데이터 정제가 함께 이루어진 결과이다.

#### Prompt v2 - 평가 데이터 확대

테스트 케이스를 10개에서 20개로 확대하여 재평가함.

- 전체 케이스: 20
- PASS: 17
- FAIL: 3
- Exact Match: 85.0%

실패 사례:

- RISK_015: 정상적인 연락처 교환을 `EXTERNAL_CONTACT`로 오탐
- RISK_017: `SUSPICIOUS_CONDITION` 대신 `PREPAYMENT_REQUEST` 탐지
- RISK_020: `SAFE_PAYMENT_REFUSAL` 미탐

분석:

- RISK_015는 `EXTERNAL_CONTACT`의 경계 조건이 부족한 것으로 판단
- RISK_017은 기존 테스트 문장이 `PREPAYMENT_REQUEST`로도 해석될 수 있어 테스트 케이스 재정의 필요
- RISK_020은 하나의 문장에 여러 위험 패턴이 존재할 때 일부 유형을 누락한 사례

10개 평가에서는 Exact Match 90.0%였지만,
정상/경계 사례와 신규 위험 유형 테스트를 추가하면서
20개 기준 Exact Match는 85.0%로 측정됨.

이는 성능이 단순히 하락했다기보다
평가 데이터 범위를 확장하면서 새로운 오탐/미탐 사례가 발견된 것으로 해석함.

---

### Prompt v3

v2의 20개 평가 결과를 기반으로 다음을 개선함.

- `EXTERNAL_CONTACT`에서 정상적인 연락처 교환 제외 규칙 추가
- 여러 위험 유형이 동시에 존재할 경우 각각 독립적으로 검사하도록 규칙 강화
- `SUSPICIOUS_CONDITION`의 경계 조건 보강
- `PREPAYMENT_REQUEST`와 `PAYMENT_PRESSURE`의 판정 경계를 추가로 명확화
- 모호했던 RISK_017 평가 문장을 `SUSPICIOUS_CONDITION` 검증 목적에 맞게 정제

최종 재평가 결과:

- 전체 케이스: 20
- PASS: 19
- FAIL: 1
- Exact Match: 95.0%

개선된 사례:

- RISK_015: 정상적인 연락처 교환에 대한 `EXTERNAL_CONTACT` 오탐 제거
- RISK_017: `SUSPICIOUS_CONDITION`과 `PREPAYMENT_REQUEST`의 평가 경계 명확화
- RISK_020: 복합 위험 거래에서 `SAFE_PAYMENT_REFUSAL` 미탐 해결

남은 문제:

- RISK_005: 안전결제 거부와 입금 재촉 상황에서
  `PAYMENT_PRESSURE`, `SAFE_PAYMENT_REFUSAL` 외에
  `PREPAYMENT_REQUEST`가 추가 탐지되는 False Positive가 남아 있음.

현재 20개 평가 기준 Exact Match 95.0%를 달성했으며,
남은 오탐 사례는 향후 평가 데이터 확대 과정에서 추가 검증할 예정임.


---

### 9/15 품질 검증 - 평가 데이터 확대

정상 거래 오탐 감소와 복합 위험패턴 탐지 성능을 검증하기 위해
평가 데이터를 20개에서 30개로 확대함.

추가 평가 범위:

- 정상적인 안전결제 거래
- 계좌이체가 선택 사항인 정상 거래
- 직거래 목적의 정상적인 연락처 교환
- 택배 발송을 위한 정상적인 개인정보 요청
- 입금 재촉과 선입금 요구의 경계
- 여러 위험 유형이 동시에 존재하는 복합 거래

평가 결과:

- 전체 케이스: 30
- PASS: 29
- FAIL: 1
- Exact Match: 96.7%

신규 추가된 RISK_021 ~ RISK_030은 모두 PASS함.

확인된 개선점:

- 정상 거래 사례에서 불필요한 위험 탐지 없음
- `PAYMENT_PRESSURE`와 `PREPAYMENT_REQUEST`의 경계 사례 정상 탐지
- 안전결제 거부, 계좌이체 전용, 외부 연락 유도 등 복합 패턴 동시 탐지 성공
- 최대 6개의 구체적 위험 유형이 동시에 존재하는 복합 사례 탐지 성공

남은 문제:

- RISK_005에서 `PREPAYMENT_REQUEST`가 추가 탐지되는 False Positive가 계속 존재함.

현재 30개 평가 기준 Exact Match 96.7%이며,
RISK_005는 알려진 경계 사례로 기록하고 향후 추가 데이터와 함께 재검증할 예정임.