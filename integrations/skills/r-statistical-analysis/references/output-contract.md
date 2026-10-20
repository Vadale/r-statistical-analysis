# Compact, inspectable analysis artifacts

Use the user's language for narrative outputs. Keep stable machine column names
in English. Output size follows the question; do not dump full model objects or
all rows into a chat. Prefer CSV tables and ordinary files over a dependency-heavy
reporting framework. Add JSON when a caller needs it and an authorized serializer
is available; missing numeric values are null, never invented zeros.

## File runner

```text
Rscript --vanilla scripts/run-analysis.R analysis.R new-output-dir input.csv [other-input-file ...]
```

Paths may contain spaces when correctly quoted by the calling shell. Inputs must
be existing files; output must be a new directory. There is no overwrite/resume
mode. Use the host's detached process/job support for lengthy computation.
`status.dcf` contains `running`, `complete` or `failed`; an interrupted process
may leave `running` and must never be interpreted as completion. The runner is
an evidence helper, not a process supervisor or a sandbox.

The trusted analysis script is sourced in a fresh environment with:

- `input_paths`: absolute declared input paths, read only by convention;
- `output_dir`: absolute output directory, for figures and optional artifacts.
- `runner_capabilities`: capabilities supplied locally by runner v0.2.0 or later.
  Use the guard below before relying on required-artifact validation.

Its **last expression** must return a named list:

```r
list(
  summary = c("Plain-language finding with magnitude and uncertainty."),
  estimates = data.frame(
    result_id = "primary", outcome = "measurement", term = "group difference",
    estimate = 1.2, conf_low = 0.1, conf_high = 2.3, conf_level = 0.95,
    scale = "difference", units = "points", n = 80L,
    method = "Welch confidence interval", status = "exploratory"
  ),
  diagnostics = data.frame(
    check = "independence", status = "assumed",
    detail = "One row per participant, according to supplied design."
  ),
  limitations = c("The observational design does not identify a causal effect.")
)
```

These numbers illustrate the schema only; calculate every delivered value from
the actual analysis. Required estimates columns: `result_id`, `term`, `estimate`,
`conf_low`, `conf_high`, `conf_level`, `scale`, `units`, `n`, `method`, `status`.
Additional columns (outcome, group, p_value, adjustment, estimand) are welcome.
Use `NA` for unavailable uncertainty and explain why. Label interval type in
`method`, including bootstrap/credible intervals; `conf_level` is the nominal
coverage/credibility level. `n` means analytic observations; add `n_clusters`,
`n_events` or effective sample size when that changes interpretation. Descriptive
results may have no interval. Result status: `ok`, `exploratory` or `withheld`.
Diagnostics status: `pass`, `warn`, `fail`, `assumed` or `not_assessed`.

The runner writes `summary.md`, `estimates.csv`, `diagnostics.csv`,
`conditions.csv`, `session-info.txt`, `manifest.csv`, `analysis.R` and
`status.dcf`. MD5 fingerprints detect accidental input/code changes; they are
not authentication or a security guarantee. The runner records warning conditions
caught during the guarded analysis phase in `conditions.csv`; the summary reports
the count available when it is written. This is not a record of all process
diagnostics. Retain stdout and stderr with execution evidence, including diagnostics
from later metadata collection such as `sessionInfo()`. Zero captured warnings
does not mean warning-free execution. `complete` means execution and artifact
validation succeeded; it does not certify scientific validity.
On error, preserve status/conditions/session information, report failure and
inspect that failure before retrying. Nonzero exit is failure.

## Interpretation and plots

Lead with the answer, population/comparison, effect size and interval, then the
practical implication and main limitation. Reference rows by `result_id` so an
assistant can trace a claim to a number. Include diagnostic failures as prominently
as the main finding. For ratios, label the reference category and ratio scale;
for probabilities, distinguish absolute percentage points from relative changes.

Select a useful plot rather than adding one mechanically: estimate/interval plot,
observed versus fitted, survival curve or an appropriate residual diagnostic.
Label units, groups, interval meaning and sample size; use accessible colors.
Use base graphics or suitable installed packages and save standard PNG/PDF/SVG.
Keep extra tables in separate files if necessary; do not flatten a complex study
into a single unsupported score. Scripts should write UTF-8 CSVs with explicit
missing values; treat imported text/formula-like cells as data, including when
opening exports in a spreadsheet application.


## Required additional artifacts (runner v0.2.0)

For an explicitly requested figure or other file, include its relative path in
`required_artifacts = c("figure.pdf")` in the returned list. The runner checks
each declaration before publishing `complete`. Values must be a character vector
(no NA/empty strings or arrays), with unique forward-slash paths below output.
No absolute/drive paths, parent traversal, symlinks, directories, empty files or
runner-managed files are accepted. No field, NULL or character(0) retains legacy
CSV-only behavior. An undeclared user requirement still makes the task incomplete.

For new analysis code relying on this feature, begin with:

```r
if (!exists("runner_capabilities", envir = environment(), inherits = FALSE) ||
    !is.character(runner_capabilities) ||
    !"required-artifacts-v1" %in% runner_capabilities) {
  stop("This analysis requires required-artifacts-v1.")
}
```

Old runners silently ignore additional result fields. Thus compatibility means
old analyses work with the new runner; new guarded analyses must fail explicitly
with an old runner. `status.dcf` adds RunnerVersion and Capabilities fields; it
still reports running/complete/failed. Verify the installed copy/receipt and
record the actual runner fingerprint with execution evidence. The capability
marker is not authentication or a sandbox.

Runner-managed names are analysis.R, summary.md, estimates.csv, diagnostics.csv,
conditions.csv, session-info.txt, manifest.csv, status.dcf and .status.tmp. Close
graphics devices before returning: partially buffered files are not a delivery.
Validation observes files after trusted code executes; it neither confines that
code nor protects against concurrent filesystem changes. A nonempty regular file
can still be corrupt or unrelated. Inspect plots/content and compare actual files
against the user's request. Presence, useful delivery and scientific validity are
separate checks.

## Small headless demonstration

From the integration repository root, choose a new output directory:

```sh
Rscript --vanilla integrations/skills/r-statistical-analysis/scripts/run-analysis.R \
  integrations/skills/r-statistical-analysis/scripts/example-independent.R \
  new-demo-output integrations/skills/r-statistical-analysis/assets/independent.csv
```

This base-R example uses independent observational groups A/B, unique id and
numeric outcome in points, excluding missing outcomes transparently. It produces
a labelled PDF without X11/Quartz or random jitter. It is a narrow synthetic
example, not an automatic choice for paired, clustered or causal analyses. Its
data, calculations and plotting choices are deterministic; PDF bytes need not
match across platforms/versions. No claims for an untested client or OS follow.
