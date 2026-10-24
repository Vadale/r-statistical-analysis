# Compare independent groups

Synthetic worked illustration; no empirical study or broad method validation.

## Input and natural request

Use the bundled [independent-group CSV](../integrations/skills/r-statistical-analysis/assets/independent.csv):
three different people in A with outcomes 1, 2, 3, and three in B with 4, 5, 6.

> Compare A and B. Each row is an independent person. Report the mean difference
> in points with uncertainty, a labelled plot and analysis code I can rerun.

## What the result should contain

The sample means are A = 2 and B = 5; B minus A is **3 points**. An executed
analysis should also report its interval method and calculated interval, group
counts, assumptions, diagnostics and limitations. It must not infer causality
or treat this tiny dataset as evidence of practical importance.

The included [demo instructions](../README.md#run-the-small-demonstration) run
the bundled example and retain estimates, diagnostics, code, input fingerprints,
session details and `group-difference.pdf`. This page is an illustration; an
assistant must execute and inspect the actual outputs before claiming a run.

## When to use another workflow

An explicitly required Python analysis stays in Python. CSV-to-JSON conversion
or calculating a single percentage does not need the statistical workflow.
