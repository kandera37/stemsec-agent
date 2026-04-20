from dataclasses import dataclass
from typing import Dict, List


@dataclass
class BenchmarkCase:
    id: str
    framework: str
    title: str
    is_safe: bool
    ambiguous: bool
    expected_findings: List[str]
    severity: Dict[str, str]
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
    findings: List[Finding]
    summary: str