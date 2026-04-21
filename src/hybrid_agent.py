import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from prompts import SEVERITY_ONLY_SYSTEM_PROMPT
from specialized_agent import load_snippet, parse_json_response
from evaluator import normalize_finding_type

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)

V1_OUTPUT_DIR = Path("outputs/specialized")


def create_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"].strip()
    return OpenAI(api_key=api_key)


def load_v1_output(case_id: str) -> dict:
    output_path = V1_OUTPUT_DIR / f"{case_id}.json"
    with output_path.open("r", encoding="utf-8") as file:
        return json.load(file)


def normalize_v1_findings(v1_output: dict) -> dict:
    normalized_findings = []

    for finding in v1_output.get("findings", []):
        normalized_findings.append(
            {
                "type": normalize_finding_type(finding["type"]),
                "severity": str(finding["severity"]).strip().lower(),
                "confidence": str(finding["confidence"]).strip().lower(),
                "evidence": finding["evidence"],
                "recommendation": finding["recommendation"],
            }
        )

    return {
        "findings": normalized_findings,
        "summary": v1_output.get("summary", ""),
    }


def build_severity_only_prompt(code: str, accepted_findings_json: str) -> str:
    return f"""
Review the following code snippet and the already accepted security findings.

Code:
```python
{code}
```

Accepted findings:
```json
{accepted_findings_json}
```

Do not add new findings.
Do not remove findings.
Only correct severity labels if needed, using the provided rubric.

Return JSON only.
""".strip()

def run_hybrid_review(case_id: str, code: str, model: str | None = None) -> dict:
    client = create_client()
    model_name = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    v1_output = load_v1_output(case_id)
    normalized_v1 = normalize_v1_findings(v1_output)
    accepted_findings_json = json.dumps(normalized_v1, ensure_ascii=False, indent=2)

    response = client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=[
            {"role": "system", "content": SEVERITY_ONLY_SYSTEM_PROMPT},
            {"role": "user", "content": build_severity_only_prompt(code, accepted_findings_json)},
        ],
    )

    content = response.choices[0].message.content
    print("HYBRID OUTPUT:\n", content)

    return parse_json_response(content)

if __name__ == "__main__":
    case_id = "F01"
    snippet_path = Path(f"data/benchmark/snippets/{case_id}.py")
    code = load_snippet(snippet_path)
    result = run_hybrid_review(case_id, code)
    print(json.dumps(result, indent=2, ensure_ascii=False))