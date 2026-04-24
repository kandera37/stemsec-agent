from dataclasses import dataclass


@dataclass
class BenchmarkCase:
    id: str
    framework: str
    title: str
    is_safe: bool
    ambiguous: bool
    expected_findings: list[str]
    severity: dict[str, str]
    short_rationale: str


@dataclass
class Finding:
    type: str
    severity: str
    confidence: str
    evidence: str
    recommendation: str


@dataclass
class AgentOutput:
    findings: list[Finding]
    summary: str