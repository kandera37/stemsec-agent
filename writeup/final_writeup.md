# StemSec Agent: A Constrained Self-Specializing Reviewer for Web Security Code Review

## 1. Problem framing

In this project, I wanted to test whether a generic LLM-based code reviewer could be turned into a more useful security reviewer for a narrow task domain.

I chose web security review for small Python backend snippets because this domain is both manageable and realistic. I am not a security expert, but cybersecurity is a field I genuinely like, and I wanted to work on a task that felt personally interesting rather than purely abstract. I also wanted something narrow enough that I could benchmark it properly instead of relying only on subjective examples.

I used Flask and FastAPI snippets because they are convenient for this kind of setup. They make it possible to build small but realistic backend examples that still cover many common web-security issues such as SQL injection, XSS, path traversal, SSRF, unsafe evaluation, and access-control mistakes.

I did not try to build a fully autonomous general agent. Instead, I approached the task in a more engineering-oriented way: start with a simple reviewer, observe its weaknesses, and then specialize it step by step in a controlled setup. I treated “evolution” in a constrained sense: not as unconstrained self-modification, but as incremental specialization driven by observed failure patterns.

## 2. Benchmark and evaluation setup

To evaluate the system, I built a benchmark of 20 labeled code snippets:

- 8 Flask cases
- 8 FastAPI cases
- 4 safe / ambiguous / mixed cases

Each benchmark case contains:
- a Python snippet
- a YAML ground-truth file with expected findings and severity labels

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

I included safe and mixed cases on purpose. Obvious vulnerable cases are useful, but they do not show the whole picture. Safe and borderline cases are important because they reveal whether the reviewer is precise or noisy.

For evaluation, I used:
- precision
- recall
- false positives
- severity match

The main goal was to compare different reviewer versions on the same benchmark and check whether specialization actually improved reviewer behavior.

## 3. Baseline reviewer

The baseline reviewer was intentionally simple:
- one system prompt
- one user prompt
- no checklist
- no critic stage
- no explicit severity rubric

This baseline already worked reasonably well on many obvious vulnerable cases. It could identify straightforward issues such as SQL injection, SSRF, XSS, IDOR, command injection, and hardcoded secrets.

At the same time, the baseline showed several weaknesses:
- inconsistent vulnerability naming
- false positives on safe or mixed cases
- overreporting of secondary findings
- unstable severity assignment

So the baseline was useful, but noisy. That made it a good starting point for specialization.

## 4. Specialization stages

### 4.1 Specialized reviewer v1

The first specialization step introduced:
- taxonomy-aware prompting
- checklist-guided review
- a critic pass over draft findings

The purpose of v1 was to make the reviewer more structured and less noisy. Instead of allowing fully free-form findings, I constrained the output to a fixed taxonomy and added a critic stage to remove unsupported findings and improve consistency.

This version improved output discipline noticeably, especially on safe and mixed cases. It was better at avoiding unnecessary findings and producing cleaner outputs.

### 4.2 Specialized reviewer v2

After v1, the main remaining weakness was severity calibration. The reviewer became better at deciding what to report, but it was still inconsistent about how severe the issue should be.

To address that, I introduced an explicit severity rubric into the critic stage.

This improved severity calibration substantially. However, it also introduced a trade-off: the severity-focused version was not as clean as v1 in terms of precision and false-positive control.

### 4.3 Hybrid variant

I also tested a hybrid variant intended to combine:
- the cleaner finding selection behavior from earlier specialization
- a separate severity recalibration step

This seemed like a reasonable idea, but in the current setup it did not outperform the stronger specialized version overall.

That was still useful, because it showed that additional architectural complexity does not automatically improve the final system.

## 5. Results

### Baseline
- avg precision: 0.79
- avg recall: 1.00
- avg false positives: 0.35
- avg severity match: 0.65

### Specialized
- avg precision: 0.85
- avg recall: 1.00
- avg false positives: 0.30
- avg severity match: 1.00

### Hybrid
- avg precision: 0.85
- avg recall: 1.00
- avg false positives: 0.30
- avg severity match: 0.90

The most important result is that specialization helped, but different specialization steps improved different aspects of reviewer behavior.

The first specialization step improved output discipline and reduced overreporting. The second step improved severity calibration. The hybrid attempt did not add a further gain.

## 6. What became clearer during the project

One thing that became much clearer during the project was how useful the safe and mixed cases were. On clearly vulnerable snippets the baseline already looked reasonably good, but safe and borderline cases exposed its weaknesses much more clearly. That is where false positives, overreporting, and inconsistency became easier to see.

Another important observation was that improving one metric did not automatically improve the others. The first specialized version clearly improved precision and reduced false positives. The second version improved severity calibration. But these improvements did not collapse into one perfect final reviewer.

The hybrid attempt was also useful for that reason. At first, it looked like combining the strengths of earlier versions should produce a stronger final system. In practice, it did not. The added complexity did not justify itself in this setup.

So the project did not end with a single perfect reviewer. Instead, it produced a more realistic result: different specialization mechanisms improved different parts of the system, and some trade-offs remained.

## 7. Case examples

A few benchmark cases illustrate the differences between versions especially well.

| Case | Baseline behavior | Specialized behavior | Takeaway |
|------|-------------------|----------------------|----------|
| S01 | Produced an unnecessary finding on a safe SQL example | Returned no findings | Specialization reduced false positives on safe cases |
| S02 | Overflagged a safe redirect case despite allowlisting | Returned no findings | Structured review improved precision on borderline-safe code |
| F05 | Found the main issue but added extra unsupported findings | Kept the main access-control issue and removed extra noise | Critic-based review reduced overreporting |
| F03 | Found path traversal but added a secondary unnecessary finding | Kept path traversal and removed the extra finding | Specialization improved output discipline without losing recall |

These cases were useful because they showed not just aggregate metric changes, but concrete behavioral differences between the versions.

## 8. Conclusion and next steps

My main conclusion is that specialization helps, but it helps in different ways depending on how the reviewer is specialized.

In this project:
- structured prompting and critic-based review made the reviewer cleaner and more consistent
- explicit severity guidance improved severity calibration
- extra architectural complexity did not automatically produce a better final reviewer

So the strongest result of the project is not that I built a perfect autonomous reviewer. It is that I was able to observe, measure, and compare how different specialization steps changed reviewer behavior.

If I had more time, I would continue in a few directions:
- separate finding validation and severity assignment more cleanly
- make the critic stricter about false positives
- add a small calibration set specifically for severity tuning
- expand the case-study-driven evaluation instead of relying mostly on aggregate metrics

Overall, the project suggests that even a small, constrained “stem agent” setup can become more useful through specialization, but also that each extra stage must justify its complexity with measurable gains.