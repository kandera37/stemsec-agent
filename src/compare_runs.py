import json
from pathlib import Path

from benchmark import load_all_cases
from evaluator import evaluate_case, load_agent_output


BASELINE_DIR = Path("outputs/baseline")
SPECIALIZED_DIR = Path("outputs/specialized")
REPORTS_DIR = Path("outputs/reports")


def average(values: list[float]) -> float:
    if not values:
        return 0.0
    return sum(values) / len(values)


def summarize(results: list[dict]) -> dict:
    return {
        "avg_precision": average([r["precision"] for r in results]),
        "avg_recall": average([r["recall"] for r in results]),
        "avg_false_positives": average([r["false_positives"] for r in results]),
        "avg_severity_match": average([r["severity_match"] for r in results]),
    }


def main() -> None:
    REPORTS_DIR.mkdir(parents=True, exist_ok=True)

    cases = load_all_cases()

    baseline_results = []
    specialized_results = []

    for case in cases:
        baseline_path = BASELINE_DIR / f"{case.id}.json"
        specialized_path = SPECIALIZED_DIR / f"{case.id}.json"

        if baseline_path.exists():
            baseline_output = load_agent_output(baseline_path)
            baseline_results.append(evaluate_case(case, baseline_output))

        if specialized_path.exists():
            specialized_output = load_agent_output(specialized_path)
            specialized_results.append(evaluate_case(case, specialized_output))

    baseline_summary = summarize(baseline_results)
    specialized_summary = summarize(specialized_results)

    comparison = {
        "baseline": baseline_summary,
        "specialized": specialized_summary,
        "baseline_case_results": baseline_results,
        "specialized_case_results": specialized_results,
    }

    report_path = REPORTS_DIR / "comparison.json"
    with report_path.open("w", encoding="utf-8") as file:
        json.dump(comparison, file, indent=2, ensure_ascii=False)

    print("=== BASELINE SUMMARY ===")
    print(json.dumps(baseline_summary, indent=2, ensure_ascii=False))

    print("\n=== SPECIALIZED SUMMARY ===")
    print(json.dumps(specialized_summary, indent=2, ensure_ascii=False))

    print(f"\nSaved comparison report to: {report_path}")


if __name__ == "__main__":
    main()