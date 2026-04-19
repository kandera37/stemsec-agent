# Evaluation plan

## Output format

Each agent run should return a structured JSON object with:

- findings
  - type
  - severity
  - confidence
  - evidence
  - recommendation
- summary

## Main evaluation dimensions

### Objective metrics
- finding precision
- finding recall
- severity match
- false positive count

### Rubric-based metrics
- evidence quality
- recommendation quality
- output structure

## Main comparison

We compare:
- baseline generic reviewer
- specialized security reviewer

on the same held-out benchmark.

## Goal

The main goal is to show whether specialization improves:
- vulnerability detection quality
- severity assessment
- output usefulness
- false positive behavior