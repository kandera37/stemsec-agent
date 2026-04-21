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

## Specialized v1 observations

The first specialized version introduced three changes compared to the baseline:
- taxonomy-aware prompting
- checklist-guided review
- a critic pass over draft findings

### What improved
The most visible improvement is output discipline.

1. **Better taxonomy consistency**
   The specialized reviewer now uses the intended benchmark labels much more consistently, such as `sql_injection`, `ssrf`, `xss`, `idor`, and `broken_access_control`.

2. **Better handling of safe cases**
   The specialized reviewer performs better than the baseline on several safe or borderline cases. In particular, it avoids some false positives that the baseline produced on safe SQL and safe redirect examples.

3. **Critic helps reduce overreporting**
   On several mixed or noisy cases, the critic removes secondary findings that are not central to the benchmark ground truth. This improves precision and makes the output more aligned with the intended evaluation setup.

### What did not improve enough
The main remaining weakness is severity calibration.

The specialized reviewer often predicts the correct vulnerability type, but the critic sometimes shifts severity in the wrong direction. In other words, the system is becoming more disciplined about *what* it reports, but not yet reliably disciplined about *how severe* the issue should be.

### Current conclusion
Specialized v1 already provides a meaningful improvement over the baseline in taxonomy consistency and false-positive control.

However, severity assignment still needs additional work, so the next improvement step should focus on a more explicit severity rubric rather than broader retrieval or more architectural complexity.

## Baseline vs specialized v1 comparison

The first quantitative comparison between the baseline reviewer and the specialized reviewer shows a clear trade-off.

### Main improvements
Compared to the baseline, specialized v1 improved:
- average precision: 0.79 → 0.975
- average false positives: 0.35 → 0.05

Importantly, recall remained at 1.0, which means the specialization improved output discipline without reducing vulnerability coverage.

### Main remaining weakness
The main regression is severity calibration:
- average severity match: 0.65 → 0.50

This suggests that the current specialization is much better at deciding **what** to report, but still not reliable enough at deciding **how severe** the issue should be.

### Interpretation
This is still a meaningful improvement overall.

The first specialization stage successfully reduced overreporting and improved taxonomy consistency, especially on safe and mixed cases. However, severity assignment remains unstable and should be the main focus of the next iteration.

## Specialized v2 observations

The second specialized iteration introduced an explicit severity rubric into the critic stage.

### What improved
The main gain of v2 is severity calibration.

Compared to the baseline and v1, severity assignment became much more consistent with the benchmark labels. In the current comparison, severity match reached 1.0.

### What regressed
However, this improvement came with a trade-off.

Compared to specialized v1, the v2 reviewer became less precise and produced more false positives:
- average precision dropped from 0.975 to 0.85
- average false positives increased from 0.05 to 0.30

### Interpretation
This suggests that explicit rubric pressure helps the critic normalize severity labels, but can also make it more willing to preserve or reinterpret findings instead of aggressively removing weak ones.

### Current conclusion
At this point, the project shows a meaningful and realistic trade-off across three stages:

- baseline: broad but noisy
- specialized v1: much cleaner and more disciplined
- specialized v2: better calibrated severity, but somewhat less strict about overreporting

This is a useful result rather than a failure, because it shows that different specialization mechanisms improve different aspects of reviewer behavior.