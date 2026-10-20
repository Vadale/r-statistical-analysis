#!/usr/bin/env python3
"""Model-free regression checks for declared files and the small R PDF example.

No network or new R packages. --evidence selects a new persistent result directory.
--baseline optionally checks the actual previous runner, without changing it.
"""
import argparse
import csv
import hashlib
import json
import math
import os
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SKILL = ROOT / 'integrations/skills/r-statistical-analysis'
RUNNER = SKILL / 'scripts/run-analysis.R'
EXAMPLE = SKILL / 'scripts/example-independent.R'
ASSET = SKILL / 'assets/independent.csv'
PROBE = '''list(summary="Artifact-contract probe; no statistical fit.",
 estimates=data.frame(result_id="probe",term="probe",estimate=0,
 conf_low=NA_real_,conf_high=NA_real_,conf_level=NA_real_,scale="probe",
 units="none",n=0,method="contract probe",status="withheld"),
 diagnostics=data.frame(check="scope",status="not_assessed",detail="No fit"),
 limitations="Contract probe."%s)
'''


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def matches_reference(actual, expected, tolerance=1e-9):
    return math.isfinite(actual) and math.isfinite(expected) and abs(actual - expected) <= tolerance


def dcf(path):
    return dict(line.split(': ', 1) for line in path.read_text().splitlines() if ': ' in line)


def run_suite(evidence, baseline):
    evidence.mkdir(parents=True, exist_ok=False)
    records = []
    errors = []
    originals = {str(p): sha(p) for p in [RUNNER, EXAMPLE, ASSET]}

    def run(name, body=None, expect=0, runner=RUNNER, input_file=None, artifact_error=False):
        case = evidence / name
        case.mkdir()
        script = EXAMPLE
        if body is not None:
            script = case / 'analysis.R'
            script.write_text(body)
        output = case / 'results'
        command = ['Rscript', '--vanilla', str(runner), str(script), str(output)]
        if input_file is not None:
            command.append(str(input_file))
        before = {str(p): sha(p) for p in [script, *([input_file] if input_file else [])]}
        process = subprocess.run(command, capture_output=True, text=True, timeout=30)
        (case / 'execution.log').write_text(process.stdout + process.stderr)
        status = dcf(output / 'status.dcf') if (output / 'status.dcf').exists() else {}
        conditions = []
        if (output / 'conditions.csv').exists():
            with (output / 'conditions.csv').open(newline='') as f:
                conditions = list(csv.DictReader(f))
        issue = []
        if process.returncode != expect:
            issue.append(f'exit {process.returncode}, expected {expect}')
        desired = 'complete' if expect == 0 else 'failed'
        if status.get('State') != desired:
            issue.append(f'state {status.get("State")}, expected {desired}')
        if artifact_error and not any('artifact' in c['message'].lower() for c in conditions if c['type'] == 'error'):
            issue.append('failure was not an explained artifact error')
        if expect and not (output / 'session-info.txt').is_file():
            issue.append('missing failure session information')
        if any(sha(Path(p)) != h for p, h in before.items()):
            issue.append('input or analysis source mutated')
        record = {'case': name, 'command': command, 'runner_sha256': sha(runner),
                  'returncode': process.returncode, 'status': status, 'errors': issue,
                  'input_sha256': before}
        records.append(record)
        errors.extend(f'{name}: {i}' for i in issue)
        return output, conditions

    def probe(name, declaration, setup='', expect=1):
        return run(name, setup + '\n' + PROBE % (',required_artifacts=' + declaration),
                   expect=expect, artifact_error=bool(expect))

    probe('valid_file', '"note.txt"', 'writeLines("a retained note", file.path(output_dir,"note.txt"))', 0)
    probe('valid_nested_spaced', '"extra files/a note.txt"',
          'dir.create(file.path(output_dir,"extra files")); writeLines("note",file.path(output_dir,"extra files/a note.txt"))', 0)
    probe('missing_file', '"missing.pdf"')
    probe('empty_file', '"empty.pdf"', 'file.create(file.path(output_dir,"empty.pdf"))')
    probe('directory', '"directory"', 'dir.create(file.path(output_dir,"directory"))')
    probe('partial_pair', 'c("one.txt","two.txt")', 'writeLines("one",file.path(output_dir,"one.txt"))')
    for name, declaration in [('list_field','list("file.pdf")'), ('na_field','NA_character_'),
                              ('empty_string','""'), ('matrix_field','matrix("file.pdf")'),
                              ('absolute','"/not/an/allowed/artifact.pdf"'), ('drive_path','"C:/outside.pdf"'),
                              ('parent_path','"../outside.pdf"'), ('sibling_prefix','"../results-sibling/file.pdf"'),
                              ('reserved','"estimates.csv"'), ('reserved_disguised','"./status.dcf"'),
                              ('duplicate','c("note.txt","./note.txt")')]:
        setup = 'writeLines("note",file.path(output_dir,"note.txt"))' if name == 'duplicate' else ''
        probe(name, declaration, setup)
    outside = evidence / 'outside'
    outside.mkdir(); (outside / 'note.txt').write_text('outside fixture')
    encoded = json.dumps(str(outside))
    probe('symlink_leaf','"note.txt"',f'file.symlink(file.path({encoded},"note.txt"),file.path(output_dir,"note.txt"))')
    probe('symlink_ancestor','"linked/note.txt"',f'file.symlink({encoded},file.path(output_dir,"linked"))')
    run('legacy_absent', PROBE % '')
    run('legacy_partial_field', PROBE % ',required_artifacts_note="Not applicable"')
    probe('legacy_empty', 'character(0)', expect=0)
    probe('legacy_null', 'NULL', expect=0)
    run('omitted_requirement', PROBE % '')
    fake, _ = probe('nonempty_not_a_pdf', '"figure.pdf"',
                    'writeLines("This is text, not a plot.",file.path(output_dir,"figure.pdf"))', 0)
    if (fake / 'figure.pdf').read_bytes().startswith(b'%PDF-'):
        errors.append('Negative fixture unexpectedly contains a PDF')
    # These completions are deliberately NOT semantic task passes.
    records[-1]['semantic_task_delivered'] = False
    records[-2]['semantic_task_delivered'] = False
    first, _ = run('demo', input_file=ASSET)
    second, _ = run('demo_rerun', input_file=ASSET)
    missing = evidence / 'missing.csv'
    missing.write_text(ASSET.read_text() + 'a4,A,NA\nb4,B,NA\n')
    missing_out, missing_conditions = run('demo_missing', input_file=missing)
    def interval4():
        lo, hi = 0., 10.
        for _ in range(100):
            t = (lo + hi)/2; u = t / math.sqrt(t*t+4)
            if .5+.75*u-.25*u**3 < .975: lo = t
            else: hi = t
        margin = (lo+hi)/2 * math.sqrt(2/3)
        return 3-margin, 3+margin
    lower, upper = interval4()
    for invalid in [float('nan'), float('inf'), -float('inf')]:
        if matches_reference(invalid, 3):
            errors.append('Non-finite value accepted by numerical comparison')
    for directory in [first, second, missing_out]:
        with (directory / 'estimates.csv').open(newline='') as f:
            row = next(csv.DictReader(f))
        for column, expected in [('estimate', 3), ('conf_low', lower), ('conf_high', upper)]:
            if not matches_reference(float(row[column]), expected):
                errors.append(f'{directory.name}: wrong {column}')
        if int(row['n']) != 6 or int(row['n_a']) != 3 or int(row['n_b']) != 3:
            errors.append('Wrong complete-case denominator')
        if not (directory / 'group-difference.pdf').read_bytes().startswith(b'%PDF-'):
            errors.append('Example did not produce a PDF')
        status = dcf(directory / 'status.dcf')
        if status.get('RunnerVersion') != '0.2.0' or status.get('Capabilities') != 'required-artifacts-v1':
            errors.append('Missing actual version/capability evidence')
    if not any(c['type'] == 'warning' and 'missing' in c['message'] for c in missing_conditions):
        errors.append('Missing-data warning not retained')
    if (first / 'estimates.csv').read_bytes() != (second / 'estimates.csv').read_bytes():
        errors.append('Numerical rerun differs')
    if baseline:
        old_runner = baseline / 'integrations/skills/r-statistical-analysis/scripts/run-analysis.R'
        old_out, old_conditions = run('new_example_old_runner', runner=old_runner, input_file=ASSET, expect=1)
        inherited = 'assign("runner_capabilities","required-artifacts-v1",envir=parent.env(environment()))\n'
        inherited += 'source(' + json.dumps(str(EXAMPLE)) + ',local=environment())$value\n'
        fake_out, fake_conditions = run('inherited_marker_not_enough', inherited, runner=old_runner, input_file=ASSET, expect=1)
        for directory, conditions in [(old_out, old_conditions), (fake_out, fake_conditions)]:
            if (directory / 'group-difference.pdf').exists() or not any('requires a runner' in c['message'] for c in conditions):
                errors.append('Old-runner capability guard did not stop before plotting')
    for name, before in originals.items():
        if sha(Path(name)) != before:
            errors.append('Candidate source or asset mutated: ' + name)
    report = {'status': 'PASS' if not errors else 'FAIL', 'errors': errors,
              'cases': records, 'case_count': len(records), 'baseline_supplied': bool(baseline), 'nonfinite_numeric_guards_checked': 3,
              'numerical_reference': 'Independent closed Student-t(df=4) CDF and arithmetic; 1e-9 absolute tolerance',
              'figure_limit': 'PDF header/presence checked here; content and meaning require separate inspection.',
              'semantic_negatives': 'Omitted declaration and non-PDF text are computational completions, not delivered plot tasks.'}
    (evidence / 'report.json').write_text(json.dumps(report, indent=2) + '\n')
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--evidence', type=Path)
    parser.add_argument('--baseline', type=Path)
    args = parser.parse_args()
    target = args.evidence.resolve() if args.evidence else Path(tempfile.mkdtemp(prefix='artifact-evidence-parent-')) / 'run'
    result = run_suite(target, args.baseline.resolve() if args.baseline else None)
    print(json.dumps({'status': result['status'], 'case_count': result['case_count'], 'errors': result['errors'], 'evidence': str(target)}, indent=2))
    raise SystemExit(0 if result['status'] == 'PASS' else 1)
