# Engineering Method Plugin Implementation Roadmap

**Goal:** Deliver the approved dual-host workflow plugin through five independently reviewable implementation blocks.

**Spec:** `docs/specs/2026-09-04-engineering-method-design.md`

**Canonical work register:** `BACKLOG.md`

## Execution order

1. `EM-001` — Foundation, manifests, test scaffold, licensing, and provenance
2. `EM-002` and `EM-003` — Project state/continuity and curated workflow skills; these may proceed in parallel after `EM-001`
3. `EM-004` — Subagent orchestration and architecture verification, consuming `EM-002` and `EM-003`
4. `EM-005` — Cross-host evaluation, public documentation, clean-install testing, and release gate

## Plan files

- `docs/plans/EM-001-foundation-and-provenance.md`
- `docs/plans/EM-002-project-state-and-continuity.md`
- `docs/plans/EM-003-curated-workflow-skills.md`
- `docs/plans/EM-004-orchestration-and-architecture.md`
- `docs/plans/EM-005-validation-and-release.md`

## Execution policy

Use the strongest available main model for architectural coordination. Delegate bounded work to the least expensive model that can complete it reliably, keep shared-interface changes serialized, and use isolated worktrees for independent write tasks. Each block ends with its own tests, review, backlog checkpoint, and commit. `EM-005` performs the cross-block integration and release verification.

## Specification coverage

| Design area | Owning implementation block |
|---|---|
| Dual Codex/Claude package, MIT license, pinned provenance | `EM-001` |
| Backlog, FEATURES, GitHub Issues, offline queue | `EM-002` |
| Compact continuity and downstream agentic-RAG seam | `EM-002`, consumed by `EM-004` |
| Exclusive Spec Kit/OpenSpec lifecycles and quality skills | `EM-003` |
| Strong coordinator, model tiers, subagents, fix convergence | `EM-004` |
| UML design/as-built analysis and integration gate | `EM-004` |
| Host adapters, behavioral evals, clean install, release docs | `EM-005` |
