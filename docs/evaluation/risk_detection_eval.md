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
