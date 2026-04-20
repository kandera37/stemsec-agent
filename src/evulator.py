from schemas import AgentOutput, BenchmarkCase


NORMALIZATION_MAP = {
    "sql injection": "sql_injection",
    "xss": "xss",
    "cross-site scripting": "xss",
    "path traversal": "path_traversal",
    "command injection": "command_injection",
    "broken access control": "broken_access_control",
    "hardcoded secret": "hardcoded_secret",
    "open redirect": "open_redirect",
    "insecure file upload": "insecure_file_upload",
    "ssrf": "ssrf",
    "server-side request forgery": "ssrf",
    "sensitive data exposure": "sensitive_data_exposure",
    "unsafe eval": "unsafe_eval",
    "sensitive config exposure": "sensitive_config_exposure",
    "idor": "idor",
    "insecure direct object reference": "idor",
}


def normalize_finding_type(finding_type: str) -> str:
    key = finding_type.strip().lower()
    return NORMALIZATION_MAP.get(key, key.replace(" ", "_"))


def extract_normalized_types(agent_output: AgentOutput) -> list[str]:
    return [normalize_finding_type(f.type) for f in agent_output.findings]


def compute_recall(case: BenchmarkCase, predicted_types: list[str]) -> float:
    expected = set(case.expected_findings)
    if not expected:
        return 1.0
    found = expected.intersection(predicted_types)
    return len(found) / len(expected)


def compute_precision(case: BenchmarkCase, predicted_types: list[str]) -> float:
    if not predicted_types:
        return 1.0 if not case.expected_findings else 0.0
    expected = set(case.expected_findings)
    correct = expected.intersection(predicted_types)
    return len(correct) / len(predicted_types)