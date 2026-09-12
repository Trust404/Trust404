# Risk Detection AI Evaluation

## 기본 정보

| 항목          | 내용                                              |
| ------------- | ------------------------------------------------- |
| 담당          | A - AI Risk Detection Engineer                    |
| 모델          | gpt-5-nano                                        |
| 평가 데이터   | data/evaluation/risk_cases.json                   |
| 테스트 케이스 | 10개                                              |
| 평가 방식     | expected_types와 실제 탐지 patterns의 Exact Match |
| 평가 대상     | Risk Detection Prompt                             |

---

## 1차 평가

### 결과

| 항목        |  결과 |
| ----------- | ----: |
| 전체 케이스 |    10 |
| PASS        |     7 |
| FAIL        |     3 |
| Exact Match | 70.0% |

### 실패 사례

| Case     | 문제                               |
| -------- | ---------------------------------- |
| RISK_001 | BANK_TRANSFER_ONLY가 추가 탐지됨   |
| RISK_005 | PREPAYMENT_REQUEST가 추가 탐지됨   |
| RISK_010 | SUSPICIOUS_CONDITION이 추가 탐지됨 |

### 분석

#### RISK_001

입력 채팅:

> 안전결제는 안 받아요. 계좌이체로만 거래합니다.

기존 Ground Truth:

```text
SAFE_PAYMENT_REFUSAL
```
