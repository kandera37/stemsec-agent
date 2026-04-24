import json
from pathlib import Path

from benchmark import load_all_cases
from hybrid_agent import run_hybrid_review
from specialized_agent import load_snippet

OUTPUT_DIR = Path("outputs/hybrid")
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

        print(f"Running hybrid reviewer on {case.id}...")
        code = load_snippet(snippet_path)

        try:
            result = run_hybrid_review(case.id, code)
        except Exception as error:
            result = {
                "error": str(error),
                "findings": [],
                "summary": "Hybrid run failed.",
            }

        output_path = OUTPUT_DIR / f"{case.id}.json"
        with output_path.open("w", encoding="utf-8") as file:
            json.dump(result, file, indent=2, ensure_ascii=False)

    print("Hybrid run finished.")


if __name__ == "__main__":
    main()