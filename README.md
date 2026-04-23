# StemSec Agent

A small experimental project exploring how a generic code-review agent can be specialized into a more structured and reliable security reviewer for Python web backend snippets.

## Project idea

This project investigates a simple stem-agent setup for **web security code review**.

The starting point is a **generic baseline reviewer** that analyzes small backend code snippets and reports security issues.
The project then introduces increasingly specialized review stages to improve:

- taxonomy consistency
- false positive control
- severity calibration

The chosen domain is narrow on purpose: **small Flask and FastAPI snippets with common web-security patterns**.

## Goal

The goal is not to build a universal agent.

The goal is to test whether a generic reviewer can be turned into a more structured and reliable **security reviewer** for a specific class of tasks.

## Benchmark

The benchmark contains **20 labeled snippets**:

- 8 Flask cases
- 8 FastAPI cases
- 4 safe / ambiguous / mixed cases

The benchmark covers issues such as:

- SQL injection
- XSS
- path traversal
- command injection
- broken access control
- IDOR
- SSRF
- insecure file upload
- hardcoded secrets
- open redirect
- sensitive data exposure
- unsafe eval
- sensitive config exposure

Each case has:

- a Python snippet in `data/benchmark/snippets/`
- a ground-truth YAML label file in `data/benchmark/cases/`

## Project stages

### 1. Baseline reviewer
A simple single-step reviewer with:
- one system prompt
- one user prompt
- no checklist
- no critic
- no severity rubric

### 2. Specialized reviewer v1
A structured reviewer with:
- taxonomy-aware prompting
- checklist-guided review
- critic pass

### 3. Specialized reviewer v2
A severity-aware reviewer with:
- explicit severity rubric in the critic stage

### 4. Hybrid reviewer
A hybrid reviewer combining:
- cleaner finding selection
- separate severity recalibration

In the current setup, it did not outperform the best specialized version overall.

## Main results

### Baseline
- avg precision: **0.79**
- avg recall: **1.00**
- avg false positives: **0.35**
- avg severity match: **0.65**

### Specialized
- avg precision: **0.85**
- avg recall: **1.00**
- avg false positives: **0.30**
- avg severity match: **1.00**

### Hybrid
- avg precision: **0.85**
- avg recall: **1.00**
- avg false positives: **0.30**
- avg severity match: **0.90**

## Key takeaways

- A generic reviewer is already useful on obvious vulnerable cases.
- Specialization significantly improves output discipline.
- Safe and mixed cases benefit from stricter review structure.
- Explicit severity guidance improves severity calibration.
- Additional architectural complexity does **not automatically** improve overall results.

## Repository structure

- `data/benchmark/cases/` — ground-truth labels for benchmark cases
- `data/benchmark/snippets/` — code snippets to review
- `data/knowledge/` — checklist and vulnerability-pattern knowledge
- `outputs/baseline/` — baseline reviewer outputs
- `outputs/specialized/` — specialized reviewer outputs
- `outputs/hybrid/` — hybrid reviewer outputs
- `outputs/reports/` — comparison summaries and reports
- `src/` — benchmark loading, prompts, agents, evaluation, runners
- `writeup/notes.md` — working project notes
- `writeup/final_writeup.md` — final write-up

## How to run

### Install dependencies
```bash
pip install -r requirements.txt
```

### Configure environment
A `.env.template` file is already included in the repository.

Copy or rename it to `.env`, then fill in your API key:

```dotenv
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4.1-mini
```

### Run baseline
```bash
python3 src/run_baseline.py
```

### Run specialized reviewer
```bash
python3 src/run_specialized.py
```

### Run hybrid reviewer
```bash
python3 src/run_hybrid.py
```

### Compare results
```bash
python3 src/compare_runs.py
```

## Current status
The project is complete enough to present:

- a benchmarked baseline reviewer
- multiple specialization attempts
- measurable before/after comparison
- a realistic trade-off between precision and severity calibration
- a final write-up and runnable project structure