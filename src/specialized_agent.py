import json
import os
from pathlib import Path

from dotenv import load_dotenv
from openai import OpenAI

from prompts import SPECIALIZED_SYSTEM_PROMPT, CRITIC_SYSTEM_PROMPT, SEVERITY_RUBRIC

ROOT_DIR = Path(__file__).resolve().parent.parent
ENV_PATH = ROOT_DIR / ".env"
load_dotenv(dotenv_path=ENV_PATH, override=True)


def load_snippet(snippet_path: Path) -> str:
    with snippet_path.open("r", encoding="utf-8") as file:
        return file.read()


def load_checklist(checklist_path: Path = Path("data/knowledge/security_checklist.yaml")) -> str:
    with checklist_path.open("r", encoding="utf-8") as file:
        return file.read()


def build_specialized_user_prompt(code: str, checklist_text: str) -> str:
    return f"""
Review the following Python web backend code snippet for security issues.

Use the checklist below as a review guide.

Checklist:
{checklist_text}

Code:
```python
{code}
```

Return JSON only.
""".strip()

def build_critic_user_prompt(code: str, draft_json: str) -> str:
    return f"""
Review the following code snippet and the draft security findings produced by another agent.

Code:
```python
{code}
```

Draft findings:

```json
{draft_json}
```

Use the following severity rubric when validating or correcting severity labels:

{SEVERITY_RUBRIC}

Please remove unsupported findings, keep supported ones, normalize labels to the allowed taxonomy, and improve severity consistency.

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

def run_specialized_review(code: str, model: str | None = None) -> dict:
    client = create_client()
    model_name = model or os.environ.get("OPENAI_MODEL", "gpt-4.1-mini")
    checklist_text = load_checklist()
    first_pass = client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=[
            {"role": "system", "content": SPECIALIZED_SYSTEM_PROMPT},
            {"role": "user", "content": build_specialized_user_prompt(code, checklist_text)},
        ],
    )

    draft_content = first_pass.choices[0].message.content
    print("SPECIALIZED DRAFT OUTPUT:\n", draft_content)

    critic_pass = client.chat.completions.create(
        model=model_name,
        temperature=0,
        messages=[
            {"role": "system", "content": CRITIC_SYSTEM_PROMPT},
            {"role": "user", "content": build_critic_user_prompt(code, draft_content)},
        ],
    )

    final_content = critic_pass.choices[0].message.content
    print("CRITIC OUTPUT:\n", final_content)

    return parse_json_response(final_content)

if __name__ == "__main__":
    snippet_path = Path("data/benchmark/snippets/F01.py")
    code = load_snippet(snippet_path)
    result = run_specialized_review(code)
    print(json.dumps(result, indent=2, ensure_ascii=False))