# Wanted AI Championship 2026

## A/B 개발 시작 전 공통 규격 합의 문서 v0.1

> 프로젝트: AI 기반 중고거래 사기 위험 분석 서비스  
> 목적: A/B가 병렬 개발하더라도 이후 통합 시 변수명, JSON 구조, Enum, 데이터 타입이 달라 생기는 문제를 방지하기 위한 공통 규격 문서

---

## 1. 전체 구조

```text
판매글 + 채팅
      │
 ┌────┴────┐
 │         │
 ▼         ▼
A AI      B AI
위험탐지   불일치/상황판단
 │         │
 └────┬────┘
      ▼
 Risk Engine
      ▼
LOW / MEDIUM / HIGH + 위험점수
      ▼
정책·대응 가이드
      ▼
최종 결과 화면
```

---

## 2. 역할 분담

### A — AI Risk Detection Engineer

핵심 질문:

> 현재 거래에서 어떤 사기 위험 신호가 나타나는가?

담당:

- LLM API 연동
- Risk Detection Prompt
- Structured Output
- 위험 패턴 탐지
- Evidence 추출
- Confidence
- Evaluation
- Prompt 개선
- FastAPI Risk Detection 모듈

### B — AI Consistency & Guidance Engineer

핵심 질문:

> 판매글과 채팅이 서로 맞는가?  
> 현재 거래 상황에서 어떤 대응이 필요한가?

담당:

- LLM API 연동
- Consistency Prompt
- Structured Output
- 판매글 ↔ 채팅 불일치 탐지
- Evidence 추출
- 거래 상황 분류
- 정책/대응 가이드 연결
- Evaluation
- Prompt 개선
- FastAPI Consistency 모듈

### 공동

- Risk Engine
- `/analyze` 통합
- Frontend
- API 연결
- 통합 테스트
- Production 배포
- 제출 자료

---

## 3. 공통 입력 규격

A와 B는 동일한 입력 데이터를 사용한다.

### API

```text
POST /analyze
```

### Request

```json
{
  "listing": "판매글 내용",
  "chat": "판매자와의 채팅 내용"
}
```

| 변수      | 타입   | 필수 | 설명                 |
| --------- | ------ | ---: | -------------------- |
| `listing` | string |    O | 중고거래 판매글      |
| `chat`    | string |    O | 판매자와의 채팅 내용 |

### 예시

```json
{
  "listing": "아이폰 15 Pro 판매합니다. 안전결제 가능합니다.",
  "chat": "안전결제는 안 받아요. 계좌이체 하시면 오늘 바로 보내드릴게요."
}
```

---

## 4. 공통 네이밍 규칙

| 대상         | 규칙               | 예시                |
| ------------ | ------------------ | ------------------- |
| JSON field   | `snake_case`       | `risk_score`        |
| Python 변수  | `snake_case`       | `listing_evidence`  |
| Enum 값      | `UPPER_SNAKE_CASE` | `PAYMENT_PRESSURE`  |
| Python 파일  | `snake_case`       | `risk_detection.py` |
| Python class | `PascalCase`       | `RiskPattern`       |
| API URL      | lowercase          | `/analyze`          |

### Confidence

`0.0 ~ 1.0` 범위로 통일한다.

```text
0.93   ✅
93     ❌
"93%"  ❌
```

### 빈 배열

데이터가 없을 경우 `null` 대신 빈 배열을 사용한다.

```json
[]
```

---

## 5. A 출력 규격

A는 판매글과 채팅에서 사기 위험 패턴을 탐지한다.

```json
{
  "patterns": [
    {
      "type": "SAFE_PAYMENT_REFUSAL",
      "label": "안전결제 거부",
      "evidence": "안전결제는 안 받아요.",
      "confidence": 0.93
    },
    {
      "type": "PAYMENT_PRESSURE",
      "label": "입금 재촉",
      "evidence": "지금 입금하시면 오늘 보내드릴게요.",
      "confidence": 0.88
    }
  ],
  "summary": "판매자가 안전결제를 거부하고 빠른 계좌이체를 요구하고 있습니다."
}
```

| 필드         | 타입        | 설명                              |
| ------------ | ----------- | --------------------------------- |
| `patterns`   | array       | 탐지된 위험 패턴 배열             |
| `type`       | enum string | 프로그램 내부 위험 유형 코드      |
| `label`      | string      | 사용자에게 보여줄 한글 명칭       |
| `evidence`   | string      | 실제 입력에서 판단 근거가 된 문장 |
| `confidence` | float       | 판단 확신도 (`0.0~1.0`)           |
| `summary`    | string      | 전체 위험 분석 요약               |

---

## 6. A 위험 패턴 Enum

초기 버전에서는 아래 유형으로 시작한다.

| Enum                    | 의미                      |
| ----------------------- | ------------------------- |
| `SAFE_PAYMENT_REFUSAL`  | 안전결제 거부             |
| `PREPAYMENT_REQUEST`    | 선입금 요구               |
| `BANK_TRANSFER_ONLY`    | 계좌이체만 요구           |
| `PAYMENT_PRESSURE`      | 빠른 입금 재촉            |
| `EXTERNAL_CONTACT`      | 외부 메신저/연락 유도     |
| `PERSONAL_INFO_REQUEST` | 개인정보 요구             |
| `SUSPICIOUS_CONDITION`  | 기타 의심스러운 거래 조건 |

위험 패턴이 없을 경우:

```json
{
  "patterns": [],
  "summary": "뚜렷한 사기 위험 신호가 탐지되지 않았습니다."
}
```

---

## 7. B 출력 규격

B는 판매글과 채팅을 비교하여 불일치와 현재 거래 상황을 분석한다.

```json
{
  "inconsistencies": [
    {
      "type": "PAYMENT_METHOD_MISMATCH",
      "listing_evidence": "안전결제 가능합니다.",
      "chat_evidence": "안전결제는 안 받아요.",
      "severity": "HIGH",
      "reason": "판매글에서 안내한 결제 방식과 실제 거래에서 요구하는 결제 방식이 다릅니다."
    }
  ],
  "trade_stage": "BEFORE_PAYMENT"
}
```

| 필드               | 타입        | 설명               |
| ------------------ | ----------- | ------------------ |
| `inconsistencies`  | array       | 탐지된 불일치 목록 |
| `type`             | enum string | 불일치 유형        |
| `listing_evidence` | string      | 판매글 쪽 근거     |
| `chat_evidence`    | string      | 채팅 쪽 근거       |
| `severity`         | enum string | 불일치 심각도      |
| `reason`           | string      | 불일치 판단 이유   |
| `trade_stage`      | enum string | 현재 거래 단계     |

---

## 8. B 불일치 Enum

| Enum                       | 의미                    |
| -------------------------- | ----------------------- |
| `PAYMENT_METHOD_MISMATCH`  | 결제방식 불일치         |
| `PRICE_MISMATCH`           | 가격 불일치             |
| `DELIVERY_METHOD_MISMATCH` | 배송방식 불일치         |
| `ITEM_CONDITION_MISMATCH`  | 상품상태 불일치         |
| `DIRECT_TRADE_MISMATCH`    | 직거래 가능 여부 불일치 |
| `OTHER_CONDITION_MISMATCH` | 기타 거래조건 불일치    |

불일치가 없을 경우:

```json
{
  "inconsistencies": []
}
```

---

## 9. Severity 규격

불일치 심각도는 다음 세 단계로 통일한다.

```text
LOW
MEDIUM
HIGH
```

JSON 내부에서는 영어 대문자 Enum을 사용한다.

```json
{
  "severity": "HIGH"
}
```

Frontend에서만 사용자 친화적인 한글로 변환한다.

```text
LOW    → 낮음
MEDIUM → 주의
HIGH   → 높음
```

---

## 10. 거래 단계 `trade_stage`

```text
BEFORE_PAYMENT
AFTER_PAYMENT
SUSPECTED_FRAUD
CONFIRMED_DAMAGE
```

| Enum               | 설명                    |
| ------------------ | ----------------------- |
| `BEFORE_PAYMENT`   | 아직 송금 전            |
| `AFTER_PAYMENT`    | 송금 완료               |
| `SUSPECTED_FRAUD`  | 사기 의심 상황          |
| `CONFIRMED_DAMAGE` | 실제 피해가 확인된 상황 |

### 추가 제안

```text
UNKNOWN
```

입력 내용만으로 거래 단계를 판단하기 어려울 때 사용하는 값.

> `UNKNOWN` 추가 여부는 개발 시작 전 A/B가 최종 합의한다.

---

## 11. 공동 Risk Engine

Risk Engine은 A와 B의 결과를 합쳐 최종 위험점수와 위험등급을 계산한다.

```text
A Risk Detection
+
B Consistency Detection
        ↓
    Risk Engine
        ↓
risk_score + risk_level
```

초기 등급 기준 예시:

```text
0~29   → LOW
30~59  → MEDIUM
60~100 → HIGH
```

가중치는 Evaluation 결과를 확인하면서 조정한다.

LLM이 최종 위험점수를 임의로 생성하게 하지 않고, 규칙 기반 Risk Engine이 계산한다.

---

## 12. 최종 `/analyze` 응답 규격

```json
{
  "risk_score": 65,
  "risk_level": "HIGH",
  "patterns": [
    {
      "type": "SAFE_PAYMENT_REFUSAL",
      "label": "안전결제 거부",
      "evidence": "안전결제는 안 받아요.",
      "confidence": 0.93
    }
  ],
  "inconsistencies": [
    {
      "type": "PAYMENT_METHOD_MISMATCH",
      "listing_evidence": "안전결제 가능합니다.",
      "chat_evidence": "안전결제는 안 받아요.",
      "severity": "HIGH",
      "reason": "판매글과 실제 거래의 결제 방식이 다릅니다."
    }
  ],
  "trade_stage": "BEFORE_PAYMENT",
  "summary": "판매자가 판매글과 다른 결제 조건을 제시하고 있습니다.",
  "checkpoints": [
    "즉시 송금하지 마세요.",
    "안전결제를 다시 요청하세요.",
    "상품 소유 인증을 요청하세요."
  ]
}
```

---

## 13. 주요 변수 정리

| 변수               | 담당             | 타입          |
| ------------------ | ---------------- | ------------- |
| `listing`          | 공통             | string        |
| `chat`             | 공통             | string        |
| `patterns`         | A                | array         |
| `type`             | A/B              | enum string   |
| `label`            | A                | string        |
| `evidence`         | A                | string        |
| `confidence`       | A                | float         |
| `summary`          | A 중심           | string        |
| `inconsistencies`  | B                | array         |
| `listing_evidence` | B                | string        |
| `chat_evidence`    | B                | string        |
| `severity`         | B                | enum string   |
| `reason`           | B                | string        |
| `trade_stage`      | B                | enum string   |
| `risk_score`       | 공동 Risk Engine | integer       |
| `risk_level`       | 공동 Risk Engine | enum string   |
| `checkpoints`      | B/Guidance       | array[string] |

---

## 14. 권장 Git 브랜치 구조

```text
main
├─ develop
│  └─ 기존 개발 기록
│
└─ develop-v2
   ├─ feature/risk-detection
   │  └─ A
   │
   └─ feature/consistency-ai
      └─ B
```

### A 주요 파일

```text
backend/app/ai/risk_detection.py
backend/app/ai/prompts/risk_prompt.py
```

### B 주요 파일

```text
backend/app/ai/consistency.py
backend/app/ai/prompts/consistency_prompt.py
backend/app/services/guidance.py
```

### 공동 파일

```text
backend/app/schemas/analysis.py
backend/app/services/risk_engine.py
backend/app/routes/analyze.py
```

---

## 15. 개발 시작 전 최종 합의 체크리스트

- [ ] 역할: A = Risk Detection / B = Consistency & Guidance
- [ ] 공통 입력 변수: `listing`, `chat`
- [ ] API: `POST /analyze`
- [ ] A 출력 JSON 구조 확정
- [ ] B 출력 JSON 구조 확정
- [ ] A 위험패턴 Enum 확정
- [ ] B 불일치 Enum 확정
- [ ] `confidence`는 `0~1`
- [ ] `severity`는 `LOW / MEDIUM / HIGH`
- [ ] `trade_stage` 값 확정
- [ ] `UNKNOWN` 추가 여부 결정
- [ ] 빈 배열은 `[]`
- [ ] Git 브랜치 확정
- [ ] A/B 작업 파일 확정
- [ ] 사용할 LLM/API 모델 확정

---

## 16. 첫날 완료 기준

공통 규격 합의 후 A와 B는 서로 기다리지 않고 동시에 개발을 시작한다.

### A

```text
판매글 + 채팅
→ LLM
→ 위험 패턴 JSON
```

### B

```text
판매글 + 채팅
→ LLM
→ 불일치 JSON
```

각자 최소 1회 정상적으로 JSON을 반환하면 첫날 목표 달성으로 본다.
