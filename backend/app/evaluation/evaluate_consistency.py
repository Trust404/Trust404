import json
from pathlib import Path

from app.ai.consistency import analyze_consistency


PROJECT_ROOT = Path(__file__).resolve().parents[3]

CASES_PATH = (
    PROJECT_ROOT
    / "data"
    / "evaluation"
    / "consistency_cases.json"
)


def load_cases():
    with open(CASES_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def evaluate():
    cases = load_cases()

    total = len(cases)
    passed = 0
    failed = 0

    print(f"\n총 {total}개 테스트 시작\n")
    print("=" * 60)

    for case in cases:
        case_id = case["case_id"]
        description = case["description"]
        listing = case["listing"]
        chat = case["chat"]
        expected_types = set(case["expected_types"])

        try:
            result = analyze_consistency(
                listing=listing,
                chat=chat,
            )

            actual_types = {
                inconsistency.type
                for inconsistency in result.inconsistencies
            }

            false_positives = actual_types - expected_types
            false_negatives = expected_types - actual_types

            is_pass = (
                not false_positives
                and not false_negatives
            )

            if is_pass:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            print(f"\n[{case_id}] {status}")
            print(f"설명: {description}")
            print(f"Expected: {sorted(expected_types)}")
            print(f"Actual:   {sorted(actual_types)}")
            print(f"Trade Stage: {result.trade_stage}")

            if false_positives:
                print(
                    f"False Positive: "
                    f"{sorted(false_positives)}"
                )

            if false_negatives:
                print(
                    f"False Negative: "
                    f"{sorted(false_negatives)}"
                )

        except Exception as error:
            failed += 1

            print(f"\n[{case_id}] ERROR")
            print(f"설명: {description}")
            print(f"오류: {error}")

        print("-" * 60)

    accuracy = (passed / total) * 100 if total else 0

    print("\n평가 완료")
    print("=" * 60)
    print(f"전체: {total}")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")
    print(f"Exact Match: {accuracy:.1f}%")


if __name__ == "__main__":
    evaluate()