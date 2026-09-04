# EM-005 Cross-Host Validation and Release Implementation Plan

> **For agentic workers:** Use `engineering-method:orchestrated-implementation` when EM-004 is available; otherwise use `superpowers:subagent-driven-development`. The strongest reviewer owns the final cross-host and architecture gate.

**Goal:** Prove one common plugin works in Codex and Claude, publish accurate documentation and attribution, and package a release only after structural, behavioral, continuity, architecture, and clean-install checks pass.

**Architecture:** Portable validation and shared fixtures run without credentials. Thin host drivers execute authenticated behavioral evaluations when enabled. Repo-local marketplace metadata provides direct GitHub installation without splitting the shared skill tree.

**Tech Stack:** Python 3.11+ standard library, shell wrappers, Codex CLI, Claude Code CLI, Git, JSON/Markdown/Mermaid.

**Spec:** `docs/specs/2026-09-04-engineering-method-design.md`

## Global Constraints

- Never claim a host works from static Markdown checks alone.
- Both host manifests expose the same `skills/` tree and semantic handoffs.
- Common skills contain no provider tool syntax or model IDs.
- GitHub content in fixtures and documentation examples is English.
- Live model evaluations are isolated, bounded, and use the least expensive model adequate for routing tests; the large-feature final review uses `strong`.
- A public release requires successful live Codex and Claude smoke evidence, not skipped tests.
- README claims only behavior demonstrated by the release gate.
- No GitHub push or release publication occurs in this plan unless separately authorized.

### Task EM-005.1: Finalize platform adapters and marketplace metadata

**Files:**

- Create: `shared/platform/{codex,claude}.md`
- Create: `.agents/plugins/marketplace.json`
- Create: `.claude-plugin/marketplace.json`
- Modify: both plugin manifests and `tests/test_validate_plugin.py`
- Create: `tests/test_platform_adapters.py`

**Adapter boundary:**

- Codex adapter alone names collaboration calls, actual spawn allowlist inspection, model/effort arguments, safe long waits, worktree detection, and native Codex memory.
- Claude adapter alone names the Agent tool, model aliases/full IDs, plugin-root variables, worktree isolation, reload behavior, and Claude memory.

- [ ] Write red tests rejecting Codex/Claude tool names or provider model IDs anywhere under `skills/`, `templates/`, or host-neutral policies.
- [ ] Test every semantic operation maps in both adapters: dispatch, follow-up/fix, status, wait, cancel, isolation, model selection, and sequential fallback.
- [ ] Add repo-local marketplace entries named `engineering-method` that resolve to the repository plugin root, include required policy/category fields, and can be consumed from a future GitHub clone. Do not invent a public repository URL in plugin manifests before a remote exists.
- [ ] Extend portable validation to cover both marketplace files and manifest identity.
- [ ] Run adapter and validator tests; commit with `git commit -m "feat: add Codex and Claude distribution adapters"`.

### Task EM-005.2: Build shared routing and workflow evaluations

**Files:**

- Create: `evals/shared/triggers/*.json`
- Create: `evals/codex/expected.json`
- Create: `evals/claude/expected.json`
- Create: `scripts/run_host_evals.py`
- Create: `tests/test_host_eval_runner.py`
- Create: `tests/e2e/run-{codex,claude}-evals`

**Required cases:** trivial docs/config edit; localized reproducible bug; bounded behavior delta; new multi-component feature; architecture migration; existing Spec Kit phase; existing OpenSpec apply phase; received review; independent failures; unsupported completion claim.

- [ ] Write red runner tests with fake host processes. Each case asserts one primary lifecycle, required supporting skills, prohibited lifecycles, expected artifacts, and no duplicate controller.
- [ ] Implement JSONL transcript parsing behind a host-driver protocol. Timeout, missing command, authentication failure, malformed output, and unexpected skill selection are explicit failures, not passes.
- [ ] Implement live drivers using syntax verified from the installed `codex exec --help` and `claude --help`; record the verified invocation in adapter docs and regression fixtures.
- [ ] Use a temporary repository and temporary host configuration roots so evaluation cannot modify user projects or global plugin configuration.
- [ ] Run fake-driver tests to green. Run live trigger evaluations on `gpt-5.6-luna` and the fastest adequate available Claude model; use stronger tiers only for cases that the routing policy classifies as architectural.
- [ ] Commit with `git commit -m "test: add cross-host workflow routing evals"`.

### Task EM-005.3: Execute the large-feature architecture fixture on both hosts

**Files:**

- Create: `tests/e2e/run-large-feature-eval`
- Create: `tests/e2e/assert_large_feature.py`
- Modify: `tests/fixtures/large-feature/` and host expected outputs.

- [ ] Write a red assertion against an incomplete recorded run. Require evidence of `specify -> plan -> UML findings -> tasks -> orchestrated slices -> as-built UML -> success/recovery integration tests -> converge -> review -> verification`.
- [ ] Assert the initial inventory return-type mismatch and missing compensation path are discovered before implementation and become stable tasks.
- [ ] Assert slice reports include file/interface ownership, test command/output, reviews, and root-cause evidence for fixes.
- [ ] Assert component, success sequence, recovery sequence, and state diagrams match final code.
- [ ] Run the same fixture through Codex and Claude with a `strong` coordinator and bounded subagent roles. Keep host outputs outside the fixture source tree until sanitized and intentionally recorded.
- [ ] Run final fixture integration tests and the assertion script for each host.
- [ ] Commit with `git commit -m "test: verify architecture workflow on both hosts"`.

### Task EM-005.4: Complete static, package, and clean-install validation

**Files:**

- Create: `tests/test_{skill_frontmatter,skill_references,no_placeholders,sources_lock,attribution,readme_contract}.py`
- Create: `scripts/{package-plugin,release-check}`
- Create: `tests/e2e/test-clean-install`
- Modify: `.gitignore`, `scripts/validate_plugin.py`

- [ ] Write red tests for invalid frontmatter, missing references, placeholders, stale hashes, lock/notice divergence, derived files without mappings, absent required README sections, and mismatched marketplace identity.
- [ ] Implement deterministic package creation excluding `.git/`, local run state, caches, test outputs, and uncommitted artifacts. `package-plugin --check` builds twice and asserts identical SHA-256 output.
- [ ] Implement clean-install tests with temporary configuration homes: validate/load Claude from the packaged directory and add/install the Codex repo marketplace without touching the user's actual marketplace.
- [ ] `release-check` runs in this order:

  ```text
  portable plugin validation
  Claude native strict validation
  all Python unit/integration tests
  Codex routing evals
  Claude routing evals
  both-host large-feature eval
  clean-install test
  reproducible package check
  git diff/working-tree check
  ```

- [ ] Live-eval skipping is allowed during development but makes `release-check` fail in release mode.
- [ ] Run all static and clean-install tests to green; commit with `git commit -m "build: add reproducible cross-host release gate"`.

### Task EM-005.5: Write the public README and finalize attribution

**Files:** Modify `README.md`, `THIRD_PARTY_NOTICES.md`, `third-party/sources.lock.json`, manifests, `FEATURES.md`, and `BACKLOG.md`.

- [ ] Extend the README contract test to require every design §16 item: problem statement, exact automatic boundaries, large-feature UML/integration flow, Codex install, Claude install, local development, backlog/Issues including English-only GitHub content, model fallback, compact continuity and downstream agentic-RAG attachment, third-party acknowledgements, MIT links, and non-endorsement.
- [ ] Write the README in English. Use only installation commands demonstrated by `test-clean-install`; do not use placeholder owner/repository URLs. If no remote exists, document local installation and defer GitHub URL examples until a remote is configured.
- [ ] Expand notices and lock mappings for every copied/adapted source file. Include upstream project, URL, full SHA, source/destination, source and destination SHA-256, modification status, copyright, complete MIT notice, and modification summary.
- [ ] Mark original work—architecture modeling, continuity implementation, adapters, tests, and original orchestration policy—as `original`, not upstream-derived.
- [ ] Update `FEATURES.md` with released capabilities only after their tests pass. Mark `EM-005` and children complete only after release evidence is fresh.
- [ ] Run README, attribution, lock, and portable validator tests; commit with `git commit -m "docs: publish plugin usage and attribution"`.

### Task EM-005.6: Run the system-architect release gate

**Files:** Modify only defects found by the gate, their covering tests, `BACKLOG.md`, and final verification record.

- [ ] Run `scripts/release-check --release` with authenticated Codex and Claude environments.
- [ ] Dispatch a `strong` system-architect reviewer over the complete branch diff, design spec, all five plan results, UML/as-built evidence, trigger matrix, and release output.
- [ ] Fix every actionable Critical or Important finding using evidence-driven fix rounds and covering tests. Re-run the narrow checks after each fix and the full release gate after integration-affecting fixes.
- [ ] Re-run `scripts/release-check --release` from a clean checkout/package.
- [ ] Run `git diff --check` and `git status --short`; preserve the final command outputs in the continuity run evidence without committing secrets or verbose logs.
- [ ] Update `BACKLOG.md` and `FEATURES.md` from verified reality.
- [ ] Commit with `git commit -m "chore: complete cross-host release verification"`.

## EM-005 Acceptance Evidence

- Codex and Claude both load the packaged common skill tree.
- Every routing case selects exactly one primary lifecycle on both hosts.
- Both hosts complete the architecture fixture with success and recovery integration tests.
- Compact recovery prevents duplicate work at all lifecycle boundaries.
- Package output is reproducible and contains complete attribution.
- README installation and behavior claims match demonstrated commands.
- No unresolved Critical or Important findings remain.
- The working tree is clean after the final verification commit.
