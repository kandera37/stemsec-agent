import json
from pathlib import Path

from schemas import AgentOutput, BenchmarkCase, Finding


NORMALIZATION_MAP = {
    "sql injection": "sql_injection",
    "xss": "xss",
    "cross-site scripting": "xss",
    "cross-site scripting (xss)": "xss",
    "path traversal": "path_traversal",
    "command injection": "command_injection",
    "broken access control": "broken_access_control",
    "missing authentication/authorization": "broken_access_control",
    "authorization bypass": "broken_access_control",
    "hardcoded secret": "hardcoded_secret",
    "hardcoded secret key": "hardcoded_secret",
    "open redirect": "open_redirect",
    "insecure file upload": "insecure_file_upload",
    "unrestricted file upload": "insecure_file_upload",
    "ssrf": "ssrf",
    "server-side request forgery": "ssrf",
    "server-side request forgery (ssrf)": "ssrf",
    "sensitive data exposure": "sensitive_data_exposure",
    "information exposure": "sensitive_data_exposure",
    "unsafe eval": "unsafe_eval",
    "code injection": "unsafe_eval",
    "sensitive config exposure": "sensitive_config_exposure",
    "debug mode exposure": "sensitive_config_exposure",
    "idor": "idor",
    "insecure direct object reference": "idor",
    "insecure direct object reference (idor)": "idor",
}


def normalize_finding_type(finding_type: str) -> str:
    key = finding_type.strip().lower()
    return NORMALIZATION_MAP.get(key, key.replace(" ", "_"))


def load_agent_output(output_path: Path) -> AgentOutput:
    with output_path.open("r", encoding="utf-8") as file:
        data = json.load(file)

    findings = [
        Finding(
            type=item["type"],
            severity=item["severity"],
            confidence=item["confidence"],
            evidence=item["evidence"],
            recommendation=item["recommendation"],
        )
        for item in data.get("findings", [])
    ]

    return AgentOutput(
        findings=findings,
        summary=data.get("summary", ""),
    )


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


def compute_false_positives(case: BenchmarkCase, predicted_types: list[str]) -> int:
    expected = set(case.expected_findings)
    predicted = set(predicted_types)
    return len(predicted - expected)


def compute_severity_match(case: BenchmarkCase, agent_output: AgentOutput) -> float:
    expected = case.severity
    if not expected:
        return 1.0

    matched = 0
    correct = 0

    for finding in agent_output.findings:
        normalized_type = normalize_finding_type(finding.type)
        if normalized_type in expected:
            matched += 1
            predicted_severity = finding.severity.strip().lower()
            expected_severity = expected[normalized_type].strip().lower()
            if predicted_severity == expected_severity:
                correct += 1

    if matched == 0:
        return 0.0

    return correct / matched


def evaluate_case(case: BenchmarkCase, agent_output: AgentOutput) -> dict:
    predicted_types = extract_normalized_types(agent_output)

    return {
        "case_id": case.id,
        "expected_findings": case.expected_findings,
        "predicted_types": predicted_types,
        "precision": compute_precision(case, predicted_types),
        "recall": compute_recall(case, predicted_types),
        "false_positives": compute_false_positives(case, predicted_types),
        "severity_match": compute_severity_match(case, agent_output),
    }