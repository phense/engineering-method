# EM-008 OpenCode integration evidence

Date: 2026-09-11. Base: `ff92f44`; bounded source-linked integration, not a new
full cross-host release acceptance. Shared skill contents and existing adapters
remain unchanged.

## Behavior and native evidence

- Red phase: new installer/hook tests failed before implementation (8 tests,
  5 failures; negative cases alone were not evidence of implementation).
- Focused verification: `python3 -m unittest tests.test_opencode_integration -v`
  passed all 9 tests (including the review regression below). Coverage includes actual installer subprocesses, check,
  idempotence, config preservation, refusal of foreign loaders/symlinked parents,
  uninstall after source deletion, real Node hook execution, and linked paths.
- OpenCode 1.18.30: install into a disposable `--config-dir`, then use the same
  `OPENCODE_CONFIG_DIR` with `opencode debug skill` redirected directly to a file.
  All 17 repository skills appeared at their original worktree locations alongside
  the 4 previously visible skills. No shared skill was copied or rewritten.
- `opencode run --model deepseek/deepseek-flash --format json` in a disposable
  fixture: real `skill` event completed for `verification-before-completion` with
  the expected repository directory. Real `bash` event executed `/usr/bin/true`,
  metadata exit `0`. The response correctly quoted the injected adapter's absence
  of session-start, transcript ingestion and compaction hooks.
- The fixture allowed skill/read and exactly `/usr/bin/true`; other tools were
  denied. The process was bounded to 150 seconds. It used existing native provider
  authentication without copying or opening credentials; this is not an isolated
  authentication or clean-home test.

## Local checks and review

The initial full suite passed 316 tests. Independent read-only review found that
text-mode comparison normalized modified CRLF loader bytes. A new regression
failed before the correction; binary comparison/writing fixed it and all 9
focused tests passed. Independent fix review reran the regression successfully
and returned `Ready`, with no unresolved findings.

A subsequent full run passed all behavior tests but exposed the inventory gate:
a feature must not reference an in-progress backlog entry. F-007 publication in
the local inventory was postponed until installation and EM-008 completion.
Final state checks are recorded after local installation.

## Limits

This proves skill discovery, additive instruction registration and one actual
DeepSeek skill invocation. It does not prove automatic routing for all prompts,
all lifecycle phases, independent multi-agent execution, architectural gates or
compaction recovery in OpenCode. T3 may need a new helper/thread to discover the
installation. Existing RAG MCP access is separate from unimplemented lifecycle
hooks. No provider settings, skill provenance hashes or release acceptance claims
were changed. Raw native transcripts remain local temporary evidence and are not
included in the repository.
