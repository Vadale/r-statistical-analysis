# R Statistical Analysis

![R Statistical Analysis: statistical questions become estimates, uncertainty, diagnostics, plots and reproducible code.](assets/hero.svg)

[Checks](https://github.com/Vadale/r-statistical-analysis-skill/actions) · [Download](https://github.com/Vadale/r-statistical-analysis-skill/releases) · [MIT](LICENSE-MIT) / [Apache 2.0](LICENSE-APACHE)

An assistant skill for turning statistical questions into executed R analysis,
interpretable estimates, uncertainty, diagnostics, plots and reproducible code.
It combines concise instructions with small R execution helpers. Ordinary work
requires neither relm nor a local language model, GPU or MCP server.

> Compare these independent groups, show the difference with uncertainty, and
> give me a plot and an analysis I can rerun.

The assistant inspects the design and data, selects appropriate R methods and
returns inspectable artifacts. Explicit language or notebook requirements take
precedence. This skill does not force R into an existing Python workflow.

## Requirements at a glance

| Component | Required for | What to prepare |
| --- | --- | --- |
| Assistant with skill/file access | Assisted analysis | A supported host, the complete skill folder and access to the files you select |
| Authorized R execution | Computing results | An existing R installation with `Rscript`, or a working R session accessible to the assistant |
| R packages | Chosen statistical method | The demo uses only packages supplied with R; specialist analyses may need additional approved packages |
| New writable output directory | Bundled file runner | A new destination; existing results are refused rather than overwritten |
| Python 3.9+ | Optional local install/verify/bundle helper and public Python tests | Standard library for the helper; it is unnecessary for the R demo or ordinary skill loading |
| Git, Node/npm or a host CLI | Only the installation route you choose | Follow that host's own requirements; these are not statistical runtime dependencies |

The verified local analysis environment is **Linux x86_64, R 4.6.1**. Other R
versions/platforms are not certified by that check; run the small demo in your
actual environment first. The skill installer does not install R or statistical
packages. Without execution access, an assistant can plan an analysis or write
code, but cannot honestly return executed results.

Ordinary statistics needs **no relm, local model, GPU, MCP server or separate
model API key**. Existing host/model access is still your choice. Data access and
permission to send excerpts or plots to a hosted assistant must be established
before using confidential inputs.

## Install with skills.sh or Gemini CLI

Use the cross-agent installer and select your host:

```sh
npx skills add Vadale/r-statistical-analysis-skill --skill r-statistical-analysis
```

Or install the Gemini CLI extension from its packaged release:

```sh
gemini extensions install https://github.com/Vadale/r-statistical-analysis-skill
```

An existing R runtime and an authorized execution environment are required. The Gemini release ZIP exposes the canonical skill under `skills/`; the repository keeps its original `integrations/skills/` layout. The installer does not install R or statistical packages.

Restart the assistant session and confirm the skill is visible before use.
These packaging instructions do not establish full-workflow testing in every
client, automatic model selection or a gallery ranking.

## Pi, DeepSeek Harness and Hermes

These clients can load the same complete [integrations/skills/r-statistical-analysis](integrations/skills/r-statistical-analysis)
folder. Keep its references, scripts, runtime source and licenses together;
copying only `SKILL.md` loses required resources.

**Pi:** install this repository as a Git package:

```sh
pi install git:github.com/Vadale/r-statistical-analysis-skill
```

**DeepSeek Harness (DSH):** from a reviewed checkout, copy the complete
`integrations/skills/r-statistical-analysis` folder to `.dsh/skills/r-statistical-analysis/`
in your target project, or to its shared `.agents/skills/r-statistical-analysis/`
location. Choose a new destination; do not replace an existing skill silently.
DSH needs the skill folder directly under a recognized skills root, rather than
the whole repository nested there. See the
[DSH skill guide](https://github.com/deepseek-ai/deepseek-harness/blob/master/docs/subsystems/skills.md).

**Hermes:** inspect the exact source, then install through Skills Hub:

```sh
hermes skills inspect skills-sh/Vadale/r-statistical-analysis-skill/r-statistical-analysis
hermes skills install skills-sh/Vadale/r-statistical-analysis-skill/r-statistical-analysis
```

If catalog search has not indexed the skill, the complete folder can also be
copied to a new `~/.hermes/skills/r-statistical-analysis/` directory
(or your configured Hermes home). See the
[Hermes skill guide](https://hermes-agent.nousresearch.com/docs/user-guide/features/skills).

Reload or restart the client and confirm that `r-statistical-analysis` appears.
Native catalog/body loading was checked with Pi 1.4.0, the DSH filesystem skill
provider 0.0.1-rc.3, and Hermes source revision `e3cc65d767e3`.
These checks do not establish automatic selection, marketplace ranking or a
complete model-driven workflow. The requirements and permissions below still apply.

## Try a natural request

Once this skill is installed and visible to your assistant, try:

> Compare groups A and B in this CSV. Each row is a different person; show the difference, uncertainty, a labelled plot and R code I can rerun.

A design-aware analysis with estimates, uncertainty, diagnostics, a useful plot and reproducible R code; missing data or methodological gaps stay visible.

See the [synthetic input/output example](examples/natural-request.md) for expected
behavior and nearby tasks that need another workflow. Automatic selection
depends on your host and model; explicit invocation remains available.

## Requirements and installation

For researchers, analysts and developers who need more than generated R code:
an executed analysis, an interpretable effect with uncertainty, and the artifacts
needed to inspect or rerun it. Suitable questions include group comparisons,
regression, repeated measures, survival and other statistical work; method-specific
packages and assumptions still need checking for each task.

![Workflow: frame the question and design; analyse with R and inspect uncertainty and diagnostics; deliver interpretable results and rerunnable artifacts.](assets/workflow.svg)

In Codex, a short installation route is:

```text
$skill-installer install https://github.com/Vadale/r-statistical-analysis-skill/tree/main/integrations/skills/r-statistical-analysis
```

Or use the local helper below. Codex supports `~/.agents/skills/` for user skills;
confirm discovery and restart if necessary. See the
[official skill guide](https://developers.openai.com/codex/skills).

Use an authorized assistant with file/execution tools and an existing R runtime.
Python 3.9+ is needed for the optional installation helper and tests; R analyses
use only the packages justified by their method. The small demo uses base R.

Start from a reviewed copy of this repository. Choose an existing skill-directory
parent recognized by your assistant; the helper does not configure discovery or
modify your personal settings. Installation copies only this skill, refuses an
existing destination, and never installs R, models or R packages.

```sh
python integrations/assistant-tools.py doctor --package stats
python integrations/assistant-tools.py install /absolute/existing/skill-directory/r-statistical-analysis
python integrations/assistant-tools.py verify /absolute/existing/skill-directory/r-statistical-analysis
```

Start a fresh assistant session and confirm that it can access the skill. Ask a
question naturally, or explicitly request the installed `r-statistical-analysis`
skill using your host's invocation mechanism. Discovery and automatic selection
are host/model behavior, not a guarantee supplied by these files.

## Run the small demonstration

The bundled [walkthrough](integrations/skills/r-statistical-analysis/references/worked-example.md)
contains the six-row synthetic CSV, exact commands, an assistant request, expected
numbers, every output file, log/status checks and rerun instructions. It is also
included inside installed skill folders and the release archive.

From a reviewed checkout, use Bash/Zsh and a **new** demo directory. If `mkdir`
fails because it exists, stop and choose another name in the following commands.

```sh
SKILL="integrations/skills/r-statistical-analysis"
Rscript --vanilla "$SKILL/scripts/inspect-environment.R" stats
mkdir "r-skill-demo"
```

```sh
Rscript --vanilla "$SKILL/scripts/run-analysis.R" \
  "$SKILL/scripts/example-independent.R" \
  "r-skill-demo/result" "$SKILL/assets/independent.csv" \
  > "r-skill-demo/stdout.log" 2> "r-skill-demo/stderr.log"
```

Accept the run only after a successful process exit, `State: complete` in
`result/status.dcf`, inspection of both logs and the actual PDF. Expected result:
**B minus A = 3 points, 95% Welch interval 0.733042 to 5.266958**, with A: n=3,
mean=2 and B: n=3, mean=5; six analysed observations, zero exclusions. This is a
small synthetic observational comparison, not a causal finding. Its distribution
and missingness assumptions are not established by a successful fit.

The nine result files include the PDF, estimates, diagnostics, captured
conditions, code, input fingerprints, session details and status. For an installed
copy, set `SKILL` to its actual directory and use the same commands; no Python or
repository helper is needed. For a repeat, choose a new result/log destination.
The [walkthrough](integrations/skills/r-statistical-analysis/references/worked-example.md)
explains what each file does and how an assistant should interpret it.

![Actual plot from the included synthetic independent-group demonstration: a mean difference and 95% Welch interval.](assets/example-group-difference.png)

## Release 0.2.2

This release consolidates requirements, the installed worked example and existing
cross-agent distribution. Skill/plugin/Gemini metadata identifies 0.2.2; the
unchanged runner still identifies its implementation as 0.2.0. Statistical code,
data and inference behavior are unchanged.

## What v0.2 adds

Analyses can declare required additional files through `required_artifacts`.
The runner refuses completion for missing, empty, directory, invalid or escaping
paths. The new example checks the runner's capability before analysing data;
older scripts continue to work with the new runner. See the
[output contract](integrations/skills/r-statistical-analysis/references/output-contract.md).

A runner completion establishes execution and contract checks, not full delivery
of every user requirement or scientific validity. The assistant still compares
actual files with the request and inspects their content. A nonempty file may be
the wrong plot. The runner executes trusted analyst code and is not a sandbox.
R computes locally, but a hosted assistant may receive excerpts, tool results and
plots; choose an authorized environment before processing private information.

## Checks and tested scope

Model-free checks need R and Python, with no model download or statistical-package
installation:

```sh
Rscript --vanilla tests/skills/r-statistical-analysis/test-runner.R .
python tests/assistant-integration/test-tools.py
python tests/skills/r-statistical-analysis/test-artifacts.py
```

The added tests include independent numerical references, missing denominators,
retained errors, one-way compatibility and negative artifact cases. Finite-value
checks reject NaN/Inf rather than accepting a vacuous tolerance comparison.
Numerical reproducibility is separate from byte-identical PDFs across systems.
The verified local analysis target is Linux x86_64/R 4.6.1. Pi, DSH and Hermes
native discovery/body loading was checked separately; those checks do not
establish a complete model-driven statistical workflow. Other runtimes/platforms
and advanced methods need their own evidence. Internal trials
are not customer validation or a statistical/security certification.

## Distribution and source

The [v0.2.2 release](https://github.com/Vadale/r-statistical-analysis-skill/releases/tag/v0.2.2)
has one generic `r-statistical-analysis-skill.zip` asset. Extract it into a new
folder: the Gemini manifest and `skills/r-statistical-analysis/` are at its root,
with the same canonical skill bytes and complete walkthrough as this repository.
Run the walkthrough with `SKILL="skills/r-statistical-analysis"` from the extracted
root. The optional Python helper and public tests remain in the GitHub source
checkout; the archive needs neither. Pi Git installs use the repository's
`package.json` mapping. Keep prior installations until the
new complete folder is verified; never merge only selected new files into an old
copy. Existing tags and archives remain available. This is a distribution archive,
not a ChatGPT plugin submission.


Create a new deterministic skill-only ZIP in an existing destination directory:

```sh
python integrations/assistant-tools.py bundle /absolute/existing/output/r-statistical-analysis.zip
```

This creates a local archive, not a marketplace submission. It includes only the
explicit skill payload and plugin metadata. Personal data, development logs,
planning and evaluation answers are not part of that payload.

Derived from the [R-ebirth companion skill](https://github.com/Vadale/R-ebirth).
See [NOTICE](NOTICE), [MIT license](LICENSE-MIT) and [Apache license](LICENSE-APACHE).
This is not the relm package and implies no R Foundation or upstream endorsement.

## Feedback and related skills

[Open an issue](https://github.com/Vadale/r-statistical-analysis-skill/issues) with a
small synthetic reproduction, expected behavior and your R/session details.
Do not attach confidential datasets or personal assistant conversations.
[Contribution guidance](CONTRIBUTING.md).

Related: [Sec-graph triage](https://github.com/Vadale/sec-graph-triage-skill) for reviewing
security-finding evidence; [AI Project Coach](https://github.com/Vadale/ai-project-coach-skill)
for improving how you work with AI. Each can be used independently.
