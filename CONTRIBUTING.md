# Contributing

Describe the concrete problem, intended behavior and relevant evidence in an
issue or pull request. Keep documentation, code comments, commits and GitHub
content in English. Do not include credentials, local state or private model
transcripts. This project uses the MIT License, copyright Peter Hense.

## Scope and review

Read the [proportionality rule](shared/policies/proportionality.md). Small edits
need focused checks; they do not need a new planning framework. Preserve stable
backlog IDs and keep `FEATURES.md` aligned with implemented capabilities. Do not
migrate this project's backlog without separate maintainer authorization.

For behavior changes, add meaningful tests for the contract or confirmed defect.
Risky or integration-bearing changes need independent review; mechanical changes
can receive coordinator review. Reuse unaffected evidence with its revision and
limits. Never weaken a failed gate to make a release appear accepted.

## Local checks

From the checkout root, using Python 3.11+ and both host CLIs for native checks:

```sh
python3 -m unittest discover -s tests -t . -v
python3 scripts/validate-plugin
claude plugin validate --strict .
python3 -m compileall -q engineering_method scripts tests
bash -n scripts/task-brief scripts/review-package
git diff --check
```

The Python suite needs no added runtime packages or model credentials.
Provenance auditing requires local upstream trees at the exact revisions in
`third-party/sources.lock.json`:

```sh
python3 scripts/audit-provenance \
  --source-root github-spec-kit=/path/to/pinned/spec-kit \
  --source-root openspec=/path/to/pinned/OpenSpec \
  --source-root superpowers=/path/to/pinned/superpowers \
  --source-root humanizer=/path/to/pinned/humanizer \
  --source-root sre-runbook-agent-skills=/path/to/pinned/sre-runbook-agent-skills \
  --source-root han=/path/to/pinned/han
```

Preserve upstream MIT notices and source mappings. If intentionally adapting a
mapped file, update its destination hash and explain the adaptation; do not
silently replace upstream revisions. Public authoring tools are not plugin
runtime dependencies; see the [authoring record](docs/verification/documentation-authoring.md).

## Bounded native routing checks

For authorized Claude model probes, use `scripts/run_host_evals.py --host claude
--native-auth --case <fixture-id> --plugin-root <unchanging-copy> --output-dir
<temporary-output>`. `--native-auth` preserves the terminal's native login
environment while disabling inherited settings, hooks and MCP. Do not substitute
`--auth-home ~/.claude` merely because it looks like the default directory:
explicitly setting `CLAUDE_CONFIG_DIR` can select a different native account.
The default isolated mode and explicit `--auth-home` remain available.

## Package and install

The packager reads committed Git blobs at `HEAD`, not unstaged or staged edits.
Commit the intended files after local checks, then run:

```sh
python3 scripts/package-plugin --check --output /tmp/engineering-method.zip
python3 tests/e2e/test-clean-install --package /tmp/engineering-method.zip
```

The packaging check builds twice and compares SHA-256. Clean installation uses
empty disposable host configurations and makes no live model requests. Review
the tracked inventory and history before a public push; packaging exclusions
alone do not prevent sensitive Git history from being published.

## Release policy

`v0.1.1` adds OpenCode with [bounded integration evidence](docs/verification/EM-008-opencode.md).
Its release notes must keep that scope separate from the historical `v0.1.0` baseline with
[independently accepted original gate coverage](docs/verification/EM-005-acceptance.md).
The historical `v0.1.0-rc.1` retains its reduced acceptance scope. Evidence reuse
must identify unchanged inputs, revisions and limitations; corrections must
remain traceable to genuine native evidence. Preserve failed original reports.
The original gate command is `python3 scripts/release-check --release
--output-dir /tmp/em-release`; it includes paid native evaluations and is not
part of routine documentation checks. Run it only with appropriate explicit
budget authorization. Do not relabel its failed or missing results as passed.
Release notes must name passed checks and unresolved limitations. Attach the
reproducible plugin package and SHA-256 checksum, then verify downloaded assets
and the actual repository, commit, tag and pre-release flag.
