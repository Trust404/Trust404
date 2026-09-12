import json
import sys
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

    selected_case_ids = set(sys.argv[1:])

    if selected_case_ids:
        cases = [
            case
            for case in cases
            if case["case_id"] in selected_case_ids
        ]

    total = len(cases)
    passed = 0
    failed = 0

    trade_stage_total = 0
    trade_stage_passed = 0

    evidence_total = 0
    evidence_passed = 0

    print(f"\n총 {total}개 테스트 시작\n")
    print("=" * 60)

    for case in cases:
        case_id = case["case_id"]
        description = case["description"]
        listing = case["listing"]
        chat = case["chat"]
        expected_types = set(case["expected_types"])
        expected_trade_stage = case.get("expected_trade_stage")

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

            types_pass = (
                not false_positives
                and not false_negatives
            )

            evidence_pass = True

            for inconsistency in result.inconsistencies:
                evidence_total += 1

                listing_evidence_valid = (
                    inconsistency.listing_evidence.strip()
                    in listing
                )
                chat_evidence_valid = (
                    inconsistency.chat_evidence.strip()
                    in chat
                )

                if (
                    listing_evidence_valid
                    and chat_evidence_valid
                ):
                    evidence_passed += 1
                else:
                    evidence_pass = False

            trade_stage_pass = True

            if expected_trade_stage is not None:
                trade_stage_total += 1

                trade_stage_pass = (
                    result.trade_stage
                    == expected_trade_stage
                )

                if trade_stage_pass:
                    trade_stage_passed += 1

            is_pass = (
                types_pass
                and evidence_pass
                and trade_stage_pass
            )

            if is_pass:
                passed += 1
                status = "PASS"
            else:
                failed += 1
                status = "FAIL"

            print(f"\n[{case_id}] {status}")
            print(f"설명: {description}")
            print(f"Expected Types: {sorted(expected_types)}")
            print(f"Actual Types:   {sorted(actual_types)}")

            if expected_trade_stage is not None:
                print(
                    f"Expected Trade Stage: "
                    f"{expected_trade_stage}"
                )
                print(
                    f"Actual Trade Stage:   "
                    f"{result.trade_stage}"
                )
            else:
                print(
                    f"Trade Stage: "
                    f"{result.trade_stage} "
                    f"(평가 제외)"
                )

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

            if (
                expected_trade_stage is not None
                and not trade_stage_pass
            ):
                print("Trade Stage Mismatch")

        except Exception as error:
            failed += 1

            print(f"\n[{case_id}] ERROR")
            print(f"설명: {description}")
            print(f"오류: {error}")

        print("-" * 60)

    exact_match = (
        (passed / total) * 100
        if total
        else 0
    )

    trade_stage_accuracy = (
        (trade_stage_passed / trade_stage_total) * 100
        if trade_stage_total
        else 0
    )

    evidence_accuracy = (
        (evidence_passed / evidence_total) * 100
        if evidence_total
        else 0
    )

    print("\n평가 완료")
    print("=" * 60)
    print(f"전체: {total}")
    print(f"PASS: {passed}")
    print(f"FAIL: {failed}")
    print(f"Overall Exact Match: {exact_match:.1f}%")
    print(
        f"Trade Stage: "
        f"{trade_stage_passed}/{trade_stage_total} "
        f"({trade_stage_accuracy:.1f}%)"
    )
    print(
        f"Evidence: "
        f"{evidence_passed}/{evidence_total} "
        f"({evidence_accuracy:.1f}%)"
    )


if __name__ == "__main__":
    evaluate()