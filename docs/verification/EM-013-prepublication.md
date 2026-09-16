# EM-013 Safe state checks and documentation routing

Date: 2026-09-16. Base: `0c158cd`. The implementation and verification below
were performed locally before publication approval. On 2026-09-16 the
maintainer authorized documentation updates, integration into the existing
GitHub default branch `main`, and a push. No new release, issue creation or
backlog migration is included.

## Read-only state check

`backlog state-check` previously shared the migration implementation with
`backlog-to-issues migrate`. A writable remote caused issue creation, local
cache replacement and archive deletion even for a status request.

The command now loads local state and detects remote availability only.
`migrate_local_backlog` retains the former migration behavior exclusively for
the explicit migration command. Authorization remains the caller's obligation;
writable GitHub access alone is not authorization.

The new CLI regression used the real local files and GitHub gateway with an
in-memory transport. Before repair it failed with 11 remote mutations instead
of zero. After repair it verifies zero remote mutations, byte-for-byte local
preservation including the archive, and retained local canonical mode. Existing
explicit migration, refresh, reconciliation and archive-history tests still pass.

Independent read-only review returned Ready with no actionable findings and
reran all 43 affected tests. A live read-only state check also reported the
writable remote while preserving the local backlog bytes and mode.

## Native selection probes

These are bounded routing/pre-draft probes, not complete writing or export
workflows. The prompts supply synthetic product facts; they do not name the
expected primary skill or Humanizer skill. Expected selections are checked
outside model prompts. The pre-draft prompts ask for sentence-level guidance
before prose begins; they do not prove prose quality across a complete draft.

Codex CLI 0.154.0 uses the existing native runner with `gpt-5.6-luna`, medium
effort, native account authentication, ignored user configuration, disposable
repositories and an unchanged staged plugin. Successful checks require actual
complete skill reads, the expected primary/supporting selection, no prohibited
selection, and a nonempty decision artifact. The report records transcript and
artifact hashes. Native transcripts remain private local evidence.

The frozen plugin fingerprint is
`47f80b6358a702e9570cce0fce2f89a7d535454e0327f6d6abb55411d2e1e1e6`.
It was copied from this working implementation before final test-matrix and
report edits. A subsequent boundary correction changes only `documentation-planning`
discovery and the existing-plan trigger guidance in `documentation-authoring`.
The existing-plan and new-set cases are repeated against a second frozen
snapshot; unaffected medium/PDF probe evidence is retained with its original
fingerprint. Both snapshot fingerprints are recorded in the JSON results.

Reproduction (substitute the host, fixture ID, native auth directory and output):

```sh
python3 scripts/run_host_evals.py --host codex \
  --case documentation-draft-preparation \
  --auth-home /path/to/native/codex-home \
  --plugin-root /path/to/unchanging/plugin-copy \
  --output-dir /tmp/em-routing-result --timeout 180
```

The five cases are `standalone-document`, `documentation-set`,
`documentation-draft-preparation`, `existing-documentation-plan` and
`documentation-pdf`. The existing-plan fixture explicitly locates its assessment
at repository-root `./decision.md` to avoid ambiguity with the plan directory.
All five cases passed, including the existing-plan case after the boundary
correction and a fresh new-set countercheck. The
[JSON report](EM-013-routing-results.json) records each accepted result.

OpenCode 1.18.30 with `deepseek/deepseek-flash` completed two native skill-tool
probes: PDF export and medium pre-draft writing including Humanizer. These
prove actual invocation and the source directory, not the full five-case Codex
contract. Disposable configuration specified this checkout's skill path,
empty MCP and plugin lists, and denied tools except skill/read/glob/grep.
The command used `opencode run --pure --dir <fixture> --model
 deepseek/deepseek-flash --format json`, with explicit `OPENCODE_CONFIG_CONTENT`,
`OPENCODE_CONFIG_DIR`, `XDG_CONFIG_HOME` and disabled Claude discovery. Native
provider authentication stayed in place without opening or copying credentials.

## Unsuccessful probes and authentication diagnosis

- Initial Codex probes were rejected because the source checkout changed during
  evaluation. They were repeated against the frozen copy; no failed result was
  relabeled as a pass.
- The first existing-plan run selected and read the required skills but wrote
  its decision in the plan directory. The root-path fixture correction is
  recorded separately; the original missing-artifact failure remains preserved.
- The root-path rerun selected `documentation-planning` as extra support for
  an accepted plan, violating the existing collision expectation. The skill
  descriptions now distinguish initial/structural planning from continuation;
  authoring explicitly consumes the accepted plan without reactivating planning.
  The expected selection was not relaxed.
- An initial OpenCode invocation without explicit `--dir` did not use the
  intended fixture/configuration. It is excluded from acceptance. The corrected
  explicit-directory probes used the native skill tool successfully.
- Claude Code 2.1.272 rejected both attempted routing calls with its native
  session limit, reporting reset at 11:40 Europe/Berlin. No skill selection ran.
  No alternate billing credential or provider was used. All five Claude cases
  were initially deferred. The authentication correction below supersedes
  that diagnosis; the limit did not establish the user terminal account quota.

## Claude retry after reported quota availability

At 11:07 CEST on 2026-09-16, all five cases were retried against an unchanged
copy of commit `48b37f5`, using the same native Claude account and Sonnet at
medium effort. Each invocation was rejected before routing with the session
limit message and the reported 11:40 Europe/Berlin reset. Native authentication
was valid. The rate-limit event identified the five-hour window and disabled
organization-level overage. No manual account switch or billing change was requested.
The JSON report retains each failed attempt and transcript hash. At that point the Claude
acceptance blocker remained open; no skill implementation was changed.

## Verification scope

Independent review of the added evaluation cases returned Ready; all existing
selection and evidence gates remain enforced. The initial state-check change
passed 318 tests; the subsequent authentication correction passes 319. The package validator and native Claude
strict manifest validator pass. Both edited skills also pass the skill-creator
validator with the existing PyYAML-capable project interpreter. Prior Quarto rendering evidence in
[EM-012](EM-012-quarto-pdf.md) remains applicable because the export skill and
template are unchanged. This report does not grant a release or publish approval.

## Native authentication correction

The user's terminal screenshot showed 5% session usage, contradicting the test
results. A native `claude auth status` comparison found different account and
organization metadata depending on whether `CLAUDE_CONFIG_DIR` was explicitly
set to the default-looking `~/.claude` path. The runner's `--auth-home` option
sets that variable. Authentication status had previously been inspected without
that variable, so the status check and routing attempts were not comparable.
No credential files or secret values were inspected or copied.

Repeating the same standalone fixture while changing only that environment
handling succeeded. Each probe already used a fresh Claude process; no terminal
restart or new login was needed. Prior limit messages remain real evidence for
the forced environment, not evidence that the user's active terminal account
was exhausted. The earlier quota conclusion was incorrect.

The runner now offers Claude-only `--native-auth`, mutually exclusive with
`--auth-home`. It preserves the caller's native configuration environment,
including absence of `CLAUDE_CONFIG_DIR`. Existing isolated defaults are
unchanged. Native authentication does not enable API keys, hooks, inherited
settings or MCP: the existing exclusions remain enforced.

```sh
python3 scripts/run_host_evals.py --host claude --native-auth \
  --case documentation-draft-preparation \
  --plugin-root /path/to/unchanging/plugin-copy \
  --output-dir /tmp/em-claude-routing-result --timeout 180
```

A regression executes the CLI-to-host boundary with both absent and inherited
configuration variables, verifies environment preservation and isolation, and
requires native evidence and a decision artifact. It failed before the new
option existed and passed after implementation. The report retains the prior
failed attempts instead of treating them as routing failures or successful tests.

The full Python suite passes 319 tests after the starter change. Independent
read-only review returned Ready, reran all 31 runner tests and verified that
Codex rejects `--native-auth` and that Claude rejects combining it with
`--auth-home`. Both rejected argument combinations exit before native calls.

All five Claude cases now pass with Sonnet at medium effort and `--native-auth`.
The unchanged snapshot fingerprint is
`1dd4b3a3ad43e36870f343dddffa71f4ebfacbae02ea4e13ec528ea9005e0994`.
Two initial native-auth attempts were rejected for missing complete skill-read
evidence; fresh repetitions passed without changing prompts, expectations or
evidence gates. Both failed transcripts remain recorded. The native checks
prove selection/preparation, including Humanizer before drafting at medium and
large scales, not full authored-document quality. EM-013 has no remaining
acceptance blocker. Publication approval was given after this verification.

## Final package and main integration

Implementation commit `89ad76c` built reproducibly as a 244-file package with
SHA-256 `1d803c95023ef01d00ca5434982adfd0ff40bf1e841de4a311ac29c31b8947b4`.
Clean installation passed for both Claude and Codex in disposable empty
configurations, without credentials or model calls. Raw transcripts and built
packages remain local; the tracked report contains bounded results and hashes.

The approved publication includes the documentation, Humanizer, PDF and
state-check/native-auth changes since remote `main` at `137306c`, followed by
this documentation refresh. The existing local `main` at `4b69c08` can advance
by fast-forward. The repository has no `master` branch. Existing version tags
and release manifests remain at `0.1.1`; a default-branch push is not a new
versioned release. Native routing and PDF rendering evidence is reused with
its recorded revisions because this refresh changes documentation only.
