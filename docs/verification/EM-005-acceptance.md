# EM-005 release acceptance — 2026-09-05

**Accepted:** all nine original gate criteria are covered for commit
`0784c79a2dfe6d087ec4da0d0ebe183355c71759`. An independent GPT-6 Astra reviewer
at low effort found no unresolved Critical or Important findings.

This is consolidated acceptance using explicitly preserved evidence from the
same unchanged package. It is **not** a claim that one invocation of
`release-check --release` succeeded. Original failed executions remain failed.
The [historical record](EM-005-completion-path.md) explains the earlier limits.

## Verified scope

| Original gate | Evidence |
| --- | --- |
| Portable validation | Passed |
| Claude strict plugin validation | Passed |
| Python tests | All 308 passed |
| Codex routing | All 12 cases passed, `gpt-6-astra`, low effort |
| Claude routing | All 12 cases passed, `claude-fable-5-1`, low effort |
| Architecture on both hosts | All ten phases, native independent reviewer responses, scope/hash checks, UML reconciliation and success/recovery integration assertions passed |
| Native clean installation | Passed in disposable configurations on both hosts |
| Reproducible packaging | Passed; 188 files |
| Clean working tree | Passed on the tested commit |

The three-upstream provenance audit also passed. Pinned revisions, MIT licensing
and third-party notices are unchanged. No active host installation was modified.

Package SHA-256:
`be0e019ea8f3153853221586f738bdcf7557e9ebb7a55b639125856a3513ad3c`.
Extracted source fingerprint:
`1edbb1d48da30c625a278ec6ccfb2bc129d8c02899361cb8b3021c11587a7638`.

## Evidence corrections and reuse

The native read collector now accommodates complete resolved skill reads and
Claude's removal of terminal newlines from Bash output. Regression controls
still reject missing instruction text. Invocation-only model/effort selections
leave installed defaults unchanged.

The package's 24 routing results and successful Codex architecture result were
reused without changing their timestamps, package, inputs or scope. The first
Claude architecture execution combined checkpoint commands and truncated output;
its failed result was preserved. Only that host's architecture case was repeated
with a temporary `--append-system-prompt` clarifying standalone checkpoint calls,
complete output, phase order and prohibition of manual checkpoint-history edits.
This supplement supplied no implementation answers and changed no assertions.

The repeated Claude run completed all ten phases, but its S2 ownership list omitted
`checkout/__init__.py`, a file explicitly included in the actual independent
reviewer's assignment and hash map. In a separate retained-artifact copy, that
single path was appended to `reports/slices.json`. No code, test, UML, checkpoint
or reviewer response changed. The original transcript and failed artifacts remain
intact. Independent replay of the unchanged packaged assertions passed on the
corrected copy; the reviewer verified the one-file metadata delta separately.

Verified architecture digests:

- Codex: `4dca7094e2850378507e02d38182e42ff1424dcdb9cae351cdefe386876819d3`.
- Claude: `cf7df70fc7d764171171dd093ece7168c08b8baa169e5cb4fe0e0c6bcb9bb7d6`.

Private evidence roots are `/tmp/em005-release-low-0784c79` and
`/tmp/em005-claude-checkpoints-0784c79`; the latter retains the exact invocation
supplement, wrapper, correction, validation script and consolidated acceptance.
Raw host transcripts are not part of the public package.

Consolidated accepted report SHA-256:
`fca1875cccb18d62edbdaa72f35a312818f7310269a76a2e314075847941419a`.
Exact Claude invocation supplement SHA-256:
`642ee8d621d4103a4d36563a90bc2c0e0f9e9f0ed76f353047bd28faa3ff340e`.

## Limits and publication boundary

Evidence covers Codex CLI 0.153.4 and Claude Code 2.1.259 and the declared fixtures.
Model compliance is not guaranteed; Claude's accepted invocation required the
explicit checkpoint supplement and the reported metadata correction. Codex's
disposable fixture had an unborn Git repository, so its native continuity recovery
failed; continuity coverage rests on the passing script tests, not that live
recovery attempt. Mermaid sources are checked semantically, not rendered.

The mistakenly migrated GitHub Issues #1–#38 were removed with explicit user
approval and their absence verified. Local backlog mode was restored; further
issue migration remains unauthorized. This cleanup is not a general GitHub
mutation acceptance test.

The existing `v0.1.0-rc.1` tag and assets remain unchanged and retain their earlier
reduced acceptance scope. This later acceptance applies to `0784c79`; it does not
retroactively certify that pre-release or publish a stable release.

The user subsequently authorized stable version `0.1.0` and the corresponding
documentation update. See the [stable publication record](EM-007-stable-release.md)
for the release package and fresh publication checks; the historical scope above
is unchanged.
