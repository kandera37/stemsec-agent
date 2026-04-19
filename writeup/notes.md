# StemSec Agent — project notes

## Working title

StemSec Agent: A Self-Specializing Agent for Web Security Code Review

## Core idea

Build a stem agent that starts as a generic code reviewer and specializes itself into a web-security reviewer for a narrow domain.

The chosen domain is security review of small Python web backend snippets written in Flask and FastAPI.

## Why this domain

This domain is narrow enough to evaluate carefully, but still rich enough to support meaningful specialization.

It also allows:
- realistic code-review style tasks
- common web vulnerability categories
- measurable before/after comparison
- clear structured outputs

## Baseline agent

The baseline agent is a generic single-agent code reviewer.

It receives:
- a code snippet
- a task asking it to identify security issues

It does not initially have:
- a dedicated security checklist
- a planner
- a critic pass
- a severity rubric
- retrieval over security patterns

## Specialization hypothesis

The stem agent can improve by selecting architectural mutations after observing recurring failure patterns on representative tasks.

## Mutation space

Planned mutations:

1. Add a planner step
2. Add a security checklist
3. Add a critic/self-review step
4. Add a severity/confidence rubric
5. Add retrieval over vulnerability patterns

## Benchmark idea

A small benchmark of 20 labeled snippets:

- 8 Flask cases
- 8 FastAPI cases
- 4 safe / ambiguous / mixed cases

The benchmark includes common web vulnerability categories such as:
- SQL injection
- XSS
- path traversal
- command injection
- broken access control
- open redirect
- insecure file upload
- SSRF
- sensitive data exposure
- unsafe eval
- IDOR

## Evaluation idea

Main comparison:
- baseline generic reviewer
- specialized security reviewer

Planned evaluation dimensions:
- finding precision
- finding recall
- false positives
- severity match
- structured output usefulness

## Important principle

This project is not about building a universal agent.
It is about building a narrow stem agent that becomes specialized for one class of problems.

## Risks to watch

- benchmark being too easy
- fake specialization with no real gain
- weak or purely qualitative evaluation
- too much prompt complexity instead of real pipeline design
- mismatch between code, results, and write-up

## What should make this project stand out

- narrow and realistic task domain
- explicit mutation space
- before/after comparison
- own benchmark
- structured evaluation
- honest discussion of failures and limitations