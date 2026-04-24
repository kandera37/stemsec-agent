from pathlib import Path

import yaml

from schemas import BenchmarkCase


def load_case(case_path: Path) -> BenchmarkCase:
    with case_path.open("r", encoding="utf-8") as file:
        data = yaml.safe_load(file)

    return BenchmarkCase(
        id=data["id"],
        framework=data["framework"],
        title=data["title"],
        is_safe=data["is_safe"],
        ambiguous=data["ambiguous"],
        expected_findings=data["expected_findings"],
        severity=data["severity"],
        short_rationale=data["short_rationale"],
    )


def load_all_cases(cases_dir: str = "data/benchmark/cases") -> list[BenchmarkCase]:
    case_paths = sorted(Path(cases_dir).glob("*.yaml"))
    return [load_case(path) for path in case_paths]


if __name__ == "__main__":
    cases = load_all_cases()
    print(f"Loaded {len(cases)} benchmark cases.")
    for case in cases[:5]:
        print(case)