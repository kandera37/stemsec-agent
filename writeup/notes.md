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

## Baseline run observations

The baseline reviewer was run on all 20 benchmark cases and produced structured JSON outputs for each snippet.

### What worked
The baseline already performs reasonably well on many obvious vulnerable cases. It correctly identifies issues such as SQL injection, SSRF, XSS, IDOR, command injection, hardcoded secrets, and path traversal in multiple benchmark snippets. This confirms that the benchmark is workable and that the baseline is not trivial or non-functional.

### Main weaknesses observed
At the same time, the baseline shows several important weaknesses that make specialization meaningful:

1. **Inconsistent vulnerability naming**
   The model often uses natural-language labels such as "SQL Injection", "Cross-Site Scripting (XSS)", or "Authorization Bypass" instead of the fixed benchmark taxonomy.

2. **False positives on safe or borderline cases**
   The baseline sometimes reports extra findings that are not part of the intended ground truth. This is especially visible on safe or mixed cases, where it tends to over-flag suspicious-looking code.

3. **Overreporting secondary issues**
   On some cases, the baseline identifies the main intended vulnerability correctly but also adds secondary findings that are not central to the benchmark design.

4. **Severity inconsistency**
   The baseline does not always match the intended severity labels, especially on medium-severity cases and borderline patterns.

### Why this is useful
These weaknesses are exactly what makes the specialization stage meaningful. The baseline is strong enough to solve obvious cases, but weak enough to justify improvements in:
- structured review discipline
- taxonomy consistency
- false positive control
- severity calibration

This supports the main project hypothesis: a generic reviewer can be improved by specializing it into a more structured web-security reviewer.