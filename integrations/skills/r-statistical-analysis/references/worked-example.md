# Complete example: two independent groups

Use this walkthrough to check an installation or understand the bundled delivery
format. It uses six synthetic observations and base R, without downloading data,
packages or models. It demonstrates execution and inspectable output, not a
validated research design. Shell commands below use Bash/Zsh syntax.

## 1. Establish the question and input

Question: how much higher is the mean outcome in group B than in group A?
Each row represents a different independent person. The outcome is measured in
points; the comparison is **B minus A**. The included `assets/independent.csv` is:

```csv
id,group,outcome
a1,A,1
a2,A,2
a3,A,3
b1,B,4
b2,B,5
b3,B,6
```

Expected columns are unique nonmissing `id`, `group` containing A/B, and numeric
`outcome`. Missing outcomes are excluded with a captured warning and an explicit
count; repeated IDs, missing groups or infinite outcomes fail this example.
It is unsuitable for paired observations, repeated measurements or clusters.
Two observed outcomes per group is only an execution minimum, not adequate
sample-size justification.

## 2. Locate the complete skill and check R

From the root of a reviewed repository checkout:

```sh
SKILL="integrations/skills/r-statistical-analysis"
Rscript --version
Rscript --vanilla "$SKILL/scripts/inspect-environment.R" stats
```

For an installed copy, replace only the first line with its actual directory,
for example `SKILL="$HOME/.agents/skills/r-statistical-analysis"`. For an extracted
release archive, use `SKILL="skills/r-statistical-analysis"` from the extracted
root. The complete folder must include `scripts/`, `assets/`, `references/` and
licenses. No repository helper, Python, API key, relm or GPU is needed to run it.

`Rscript` must resolve in the execution environment where the assistant works,
which may differ from your own terminal or a restricted chat session. The check
reports the R/platform identity and whether `stats` is available; install nothing
automatically. This walkthrough was executed on Linux x86_64 with R 4.6.1.

## 3. Execute with logs and a new output directory

Create a new parent for this demonstration:

```sh
mkdir "r-skill-demo"
```

If it already exists, stop and choose a different name in all commands below.
Keep the two logs outside the runner's output directory so early failures are
also retained. Execute:

```sh
Rscript --vanilla "$SKILL/scripts/run-analysis.R" \
  "$SKILL/scripts/example-independent.R" \
  "r-skill-demo/result" "$SKILL/assets/independent.csv" \
  > "r-skill-demo/stdout.log" 2> "r-skill-demo/stderr.log"
```

The runner creates `result`; do not create it first. A nonzero process exit is a
failure, even if some files exist. Read both logs before accepting the result.

Check the final status and inspect the estimates:

```sh
Rscript --vanilla -e 's <- read.dcf("r-skill-demo/result/status.dcf"); stopifnot(s[1,"State"] == "complete"); print(read.csv("r-skill-demo/result/estimates.csv"))'
```

Expected status fields include `State: complete`, `RunnerVersion: 0.2.0` and
`Capabilities: required-artifacts-v1`. Release 0.2.2 updates documentation and
packaging; the unchanged runner still reports its own 0.2.0 implementation version.

## 4. Read and interpret the result

| Quantity | Expected value |
| --- | --- |
| Group A: n, mean | 3, 2 points |
| Group B: n, mean | 3, 5 points |
| Mean difference, B minus A | 3 points |
| 95% Welch confidence interval | 0.733042 to 5.266958 points |
| Raw / analysed / excluded observations | 6 / 6 / 0 |

The arithmetic is checkable: both sample variances are 1, the standard error is
`sqrt(1/3 + 1/3)`, and the Welch degrees of freedom are 4. The 95% interval is
`3 +/- 2.7764451052 * sqrt(2/3)`. CSV values should agree to rounding; PDF bytes,
timestamps and session metadata can differ between environments.

An appropriate answer is: “In these six synthetic observations, group B averages
3 points higher than A (95% Welch interval 0.733 to 5.267 points). This comparison
does not establish a causal effect or practical importance. Independence was
supplied by the example's design; distribution and missingness assumptions were
not established by the successful calculation.”

The PDF plots that difference and interval against a zero reference line. Open
it and inspect its labels, units, comparison direction and interval; nonempty
file presence alone does not establish a useful figure. The small artificial
dataset is not evidence about real people or an automatically suitable model
for a new dataset.

## 5. Inspect the delivered files

| File in `result/` | What to inspect |
| --- | --- |
| `summary.md` | Finding, denominators, limitations and captured-analysis warning count |
| `estimates.csv` | Difference, confidence limits, units, group counts and excluded count |
| `diagnostics.csv` | Independence is assumed; distribution/missingness are not assessed |
| `group-difference.pdf` | Actual labelled estimate/interval plot |
| `conditions.csv` | Conditions captured while the analysis ran, including any missing-outcome warning |
| `analysis.R` | Copy of the exact analysis code |
| `manifest.csv` | Declared input/code paths and MD5 fingerprints |
| `session-info.txt` | R, platform and session/package details |
| `status.dcf` | Execution state, runner version and capability |

There are nine files for this example. `conditions.csv` can contain only a header
when no analysis warning/error is captured; later process diagnostics can still
appear in `stderr.log`. `complete` confirms execution and declared-artifact checks,
not scientific validity or fulfillment of every possible user request. The
trusted-code runner is not a sandbox. Input paths in the manifest refer to the
actual input; the runner does not copy the dataset into the output folder.

## 6. Rerun or ask an assistant

Repeat the execution command with `r-skill-demo/rerun` instead of
`r-skill-demo/result` and distinct log filenames. Reusing `result` is deliberately
refused; preserve it and choose a new destination. To reuse the delivered
`result/analysis.R`, supply it to the same runner with the original CSV and a
new destination. Numerical results should agree; a changed input or analysis
requires a new interpretation rather than copying the old answer.

In an assistant with the complete skill visible and authorized file/execution
access, provide the actual paths and ask:

> Use r-statistical-analysis on the included independent.csv. Each row is a
> different independent person; outcome is in points. Compare B minus A using a
> 95% interval. Execute the bundled example into a new directory, retain stdout
> and stderr, inspect the PDF and diagnostics, and give me the finding, limits
> and links to rerunnable artifacts. Do not overwrite an existing result.

Use your host's explicit invocation syntax if needed (for example
`$r-statistical-analysis` in Codex). Without execution access, the assistant can
provide a plan/code but must not report this example as executed. For your own
data, first establish its design/schema and sharing permission; R's local
computation does not prevent excerpts or plots entering a hosted model's context.

If R is missing, prepare it separately or choose an authorized R environment.
If the capability guard fails, the installed runner is too old for this example;
install a complete current copy into a new location. For a failed analysis,
preserve status/conditions/logs and inspect the cause before a retry. The full
[output contract](output-contract.md) describes custom analyses and artifacts.
