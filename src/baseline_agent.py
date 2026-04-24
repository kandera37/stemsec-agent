import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from prompts import BASELINE_SYSTEM_PROMPT

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


def load_snippet(snippet_path: Path) -> str:
    with snippet_path.open("r", encoding="utf-8") as file:
        return file.read()


def build_user_prompt(code: str) -> str:
    return f"""
Review the following Python web backend code snippet for security issues.

Code:
```python
{code}
```
Return JSON only.
""".strip()


def create_client() -> OpenAI:
    api_key = os.environ["OPENAI_API_KEY"].strip()
    return OpenAI(api_key=api_key)


def parse_json_response(content: str) -> dict:
    content = content.strip()
    if content.startswith("```json"):
        content = content.removeprefix("```json").strip()
    elif content.startswith("```"):
        content = content.removeprefix("```").strip()

    if content.endswith("```"):
        content = content[:-3].strip()

    return json.loads(content)


def run_baseline_review(code: str, model: str | None = None) -> dict:
    client = create_client()
    model_name = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")

    response = client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=[
            {"role": "system", "content": BASELINE_SYSTEM_PROMPT},
            {"role": "user", "content": build_user_prompt(code)},
        ],
    )

    content = response.choices[0].message.content
    print("RAW MODEL OUTPUT:\n", content)

    return parse_json_response(content)


if __name__ == "__main__":
    snippet_path = Path("data/benchmark/snippets/F01.py")
    code = load_snippet(snippet_path)
    result = run_baseline_review(code)
    print(json.dumps(result, indent=2, ensure_ascii=False))