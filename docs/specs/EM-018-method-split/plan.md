# Implementation Plan: Method split

## Stable work ID

EM-018; specification: `docs/specs/EM-018-method-split/spec.md`.

## Summary and ownership

Use committed, explicit exports from `phense/method-core`. Each consumer vendors the same relative paths at its package root and pins a Git revision plus file hashes and modes in `method-core.lock.json`. This preserves existing installed-relative skill links, wrapper imports and project data without runtime coupling.

| Canonical repository | Owned paths/responsibilities |
|---|---|
| method-core | `shared/platform/`; common authority, continuity, proportionality, model-routing and playbook policies; reviewer brief; eight support skills listed below; `templates/playbooks/`; `engineering_method/`; generic state, sync, packaging, validation and OpenCode tools; their characterization/integration tests. |
| engineering-method | Spec Kit, OpenSpec, architecture, debugging and TDD skills; engineering graphs/policies, architecture/engineering templates, historical specs/releases/evidence and engineering host evaluation fixtures. |
| writing-method | Ten documentation/didactic skills; writing depth and reader-output policies, writing filter, documentation/PDF templates, writing graph and writing evaluations/tests. |

Shared support skills: project-backlog, verification-before-completion, dispatching-parallel-agents, using-git-worktrees, requesting-code-review, receiving-code-review, playbook-authoring, playbook-review. Playbooks become method-neutral; engineering lifecycle hooks move into engineering-owned policy and writing receives its own hooks. Adapters load method-local lifecycle instructions when present, with no hard dependency on writing skills. Core is a source dependency, not an installed plugin. Both plugins expose identical shared support under their own namespaces; choose the invoking method's namespace.

## Project gates and technical context

- Python >=3.11, dependency-free state/validation tooling; Node for actual OpenCode-hook tests.
- Original baseline: `d458f6a`, 319 tests passed on 2026-11-13. Preserve existing CLI/data/import contracts.
- Work is isolated on `em-018-method-split`; new sibling repositories start on `main` with no inherited secrets or runtime state.
- Existing EM-018 is coordinator-only. Implementation stays sequential. A separately tracked observed acceptance-review run can supply independent review without changing or delegating from that implementation run.
- Writing scale is medium per standalone README/reference page; no manual, PDF deliverable or new documentation-set lifecycle is required.
- No backend/API/library upgrade, model invocation or provider-account change is needed.

## Interface contracts and failure behavior

IC-001: `method-core.json` explicitly lists exports. `scripts/sync-core --source-root PATH --target-root PATH [--revision SHA]` reads immutable Git blobs, refuses dirty exported content, validates safe unique paths/modes, preflights existing ownership and stages a complete update. Before applying managed writes, persist complete original backups. Sync and recovery share one stable OS lock. On failure restore prior bytes/modes/lock; retain backups if restoration fails or the process dies. `scripts/sync-core --recover` restores a dead owner transaction offline and refuses an active owner. Check journal identity before atomic retirement; never delete the persistent `.method-core-sync.lock` during use. `scripts/sync-core --check` validates the installed lock offline. Unknown target files remain untouched.

IC-002: Existing wrappers and `engineering_method` keep their names and project cwd behavior. State path stays `.engineering-method/`, including in writing projects, as a compatibility contract.

IC-003: Plugin manifests stay native to Claude/Codex. Packaging uses the committed manifest identity. OpenCode installer derives a validated method identity for distinct loader filenames; user settings remain untouched. Native clean installs use disposable homes, not real authentication/configuration.

IC-004: Shared playbooks retain Drafted/Reviewed/Rehearsed distinctions. Generic policy never requires absent method skills. Each method owns its lifecycle routing and the decision to require playbooks.

## Tests and rollback

1. Characterization-green baseline before changing runtime ownership.
2. Red/green sync tests: offline tamper detection, dirty-source refusal, traversal/symlink/ownership conflicts, transactional failure recovery, executable bits and updates.
3. Existing runtime tests in Core and consumer packages; owned lifecycle/contract tests in each method.
4. Isolated extracted-package checks: no sibling resources; validate every skill link, core lock and wrapper execution; preserve continuity after moving packages.
5. Coexistence tests execute both OpenCode hooks and prove distinct loader ownership.
6. Verify licenses and hashes using retained immutable upstream metadata; update only changed destination hashes.
7. Package archives build twice from immutable commits and match. Source rollback is the original Git revision; consumer rollback syncs an older pinned core revision after verifying no local managed edits. Global installed plugins are unchanged during development.

## Architecture findings and supporting artifacts

`docs/uml/em-018-components.md` answers responsibility ownership and runtime independence. `docs/uml/findings.md` records AF-018-001 (shared policy must not depend on absent method), AF-018-002 (transactional sync/ownership), AF-018-003 (coexistence identity). No database model or speculative research artifact is needed.

## Dependencies and order

Core sync behavior and common exports precede consumer split. Consumers precede joint integration. Independent review and fixes precede final source publication/handoff. Source manifests and attribution are complete before packaging. Gemini adapter remains a future backlog item.

## Playbook obligations

No development operation requires an additional playbook: no live cutover/data migration or multi-actor production change occurs. The transactional sync tool and README update/rollback steps cover this reversible operation. No system playbook beyond the reusable delivered skills/templates is requested. Reassess if installation into live global profiles is added.
