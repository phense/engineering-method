# Backlog

This is the canonical task register until the repository is connected to GitHub Issues. Keep stable IDs unchanged, sort blockers first, then priority, then dependency order, and update this file at work start, scope changes, blockers, completed implementation slices, and final handoff.

## Status legend

- `⭕` Open
- `🔄` In progress
- `✅` Complete
- `❌` Blocked

## Priority directive

- `P0`: Blocks other planned work or requires immediate attention
- `P1`: Next implementation work
- `P2`: Planned after the core is operational
- `P3`: Later improvement

When an item becomes blocked, move it into the blocker-first section with the item that can remove the block immediately above it. Never renumber an existing ID when order or priority changes.

## P0 — Foundation

- ✅ `EM-001` **P0** Establish the dual-host plugin foundation and provenance controls. Blocks `EM-002` through `EM-005`.
  - ✅ `EM-001.1` Create compatible Codex and Claude plugin manifests.
  - ✅ `EM-001.2` Add the dependency-free Python validation and test scaffold.
  - ✅ `EM-001.3` Pin upstream revisions and implement MIT attribution controls.
  - ✅ `EM-001.4` Add baseline structural validation for both hosts.

## P1 — Core capabilities

- 🔄 `EM-002` **P1** Implement durable project state and compact continuity. Depends on `EM-001`.
  - 🔄 `EM-002.1` Add state models and safe filesystem primitives.
  - ⭕ `EM-002.2` Implement stable local backlog parsing, sorting, and archiving.
  - ⭕ `EM-002.3` Maintain the non-duplicative `FEATURES.md` capability inventory.
  - ⭕ `EM-002.4` Add the testable GitHub boundary.
  - ⭕ `EM-002.5` Implement idempotent issue migration, relationships, cache, and offline reconciliation.
  - ⭕ `EM-002.6` Implement versioned compact-continuity checkpoints and events.
  - ⭕ `EM-002.7` Wire project-state commands and the `project-backlog` skill.
- 🔄 `EM-003` **P1** Build the curated, non-overlapping lifecycle and quality skills. Depends on `EM-001`.
  - 🔄 `EM-003.1` Define exclusive lifecycle contracts and artifact templates.
  - ⭕ `EM-003.2` Adapt Spec Kit `specify`, `plan`, `tasks`, and `converge`.
  - ⭕ `EM-003.3` Adapt OpenSpec `propose`, `apply`, and `archive`.
  - ⭕ `EM-003.4` Port Superpowers debugging, TDD, and verification.
  - ⭕ `EM-003.5` Port review, worktree, and parallel-dispatch support.
  - ⭕ `EM-003.6` Integrate project-backlog support and collision acceptance.
- ⭕ `EM-004` **P1** Add efficient subagent orchestration and the architecture gate. Depends on `EM-002` and `EM-003`.
  - ⭕ `EM-004.1` Add shared model roles, host adapters, and agent-role briefs.
  - ⭕ `EM-004.2` Implement cohesive-slice orchestration with targeted review and evidence-driven fix loops.
  - ⭕ `EM-004.3` Implement evidence-driven defect convergence.
  - ⭕ `EM-004.4` Implement design-time and as-built UML analysis under `docs/uml/`.
  - ⭕ `EM-004.5` Add the system-architect integration-test gate.
  - ⭕ `EM-004.6` Verify recovery across compaction and subagent lifecycle boundaries.

## P2 — Release readiness

- ⭕ `EM-005` **P2** Validate, document, and package the complete plugin. Depends on `EM-001` through `EM-004`.
  - ⭕ `EM-005.1` Finalize platform adapters and marketplace metadata.
  - ⭕ `EM-005.2` Add Codex/Claude trigger, collision, fallback, and workflow evaluations.
  - ⭕ `EM-005.3` Execute the large-feature architecture fixture on both hosts.
  - ⭕ `EM-005.4` Complete static, package, and clean-install validation.
  - ⭕ `EM-005.5` Write and verify the public README and third-party notices.
  - ⭕ `EM-005.6` Run the system-architect release gate.

## Completed

- ✅ `EM-000` **P0** Approve and commit the consolidated plugin design (`877a7ea`).
