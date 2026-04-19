# StemSec Agent

A stem-agent prototype for security review of small Python web backend code snippets.

## Project idea

This project explores whether a generic code-review agent can specialize itself into a more effective web-security reviewer for a narrow class of tasks.

The target domain is security review of small **Flask** and **FastAPI** backend snippets for common web vulnerabilities such as SQL injection, XSS, path traversal, broken access control, SSRF, and unsafe code execution.

The project starts with a simple baseline agent and then introduces a specialization process that can add structured review steps such as planning, security checklists, critic passes, severity scoring, and retrieval over vulnerability patterns.

## Goal

The goal is to compare:

- a **generic baseline agent**
- a **specialized security-review agent**

and measure whether specialization improves vulnerability detection quality on a small benchmark.

## Planned approach

The project includes:

- a benchmark of labeled Flask/FastAPI snippets
- a generic baseline reviewer
- a mutation-based specialization process
- before/after evaluation
- analysis of strengths, weaknesses, and failure modes

## Repository structure

- `data/benchmark/cases/` — ground-truth labels for benchmark cases
- `data/benchmark/snippets/` — code snippets to review
- `data/knowledge/` — checklist and vulnerability-pattern knowledge
- `outputs/` — baseline and specialized outputs, reports
- `src/` — benchmark loading, agent logic, evaluation code
- `writeup/` — notes and final write-up materials

## Status

Work in progress.
Current stage:
- project structure created
- benchmark taxonomy defined
- benchmark cases are being formalized