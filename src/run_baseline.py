import json
from pathlib import Path

from baseline_agent import load_snippet, run_baseline_review
from benchmark import load_all_cases


OUTPUT_DIR = Path("outputs/baseline")
SNIPPETS_DIR = Path("data/benchmark/snippets")


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    cases = load_all_cases()
    print(f"Loaded {len(cases)} cases.")

    for case in cases:
        snippet_path = SNIPPETS_DIR / f"{case.id}.py"
        if not snippet_path.exists():
            print(f"Skipping {case.id}: snippet file not found")
            continue

        print(f"Running baseline on {case.id}...")
        code = load_snippet(snippet_path)

        try:
            result = run_baseline_review(code)
        except Exception as error:
            result = {
                "error": str(error),
                "findings": [],
                "summary": "Baseline run failed."
            }

        output_path = OUTPUT_DIR / f"{case.id}.json"
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(result, file, indent=2, ensure_ascii=False)

    print("Baseline run finished.")


if __name__ == "__main__":
    main()