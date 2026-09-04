---
name: speckit-plan
description: "Use when an existing Spec Kit spec.md is complete and needs an evidence-grounded technical plan. Not for writing requirements, implementing code, or planning a bounded OpenSpec change."
---

# Spec Kit Plan

Translate an approved feature specification into an evidence-grounded technical
plan while keeping requirements and implementation separate.

## Recovery preamble

Before creating or updating an artifact:

1. Look for a relevant `.engineering-method/runs/<work-id>/state.json` and
   `resume.md`.
2. Compare recorded commits, worktree, artifacts, and canonical task state with
   the repository.
3. Repository evidence wins over stale checkpoint or memory data.
4. Preserve validated completed work and never redispatch completed work after
   compaction or resumption.
5. Continue the recorded next action when it still matches current evidence;
   otherwise reconstruct the phase from git and canonical artifacts.

Checkpoint initialization and writes become operational only after EM-002 and
Task 6 integration. Until then, use existing checkpoint files read-only when
present, recover from repository artifacts when absent, and do not claim
checkpoint continuity is operational.

## Trigger

Use when `specs/<stable-feature-id>-<name>/spec.md` exists, satisfies its
acceptance contract, and has no current `plan.md`, or when repository evidence
requires that plan to be updated before architecture analysis.

## Do not use for

- Creating or clarifying feature requirements; use `speckit-specify`.
- Implementing any plan or task.
- A bounded existing-capability delta owned by OpenSpec.

## Consumes

- `specs/<stable-feature-id>-<name>/spec.md`.
- Applicable project gates, repository structure, code, tests, and interfaces.
- Existing validated research or design evidence for the same feature.

## Produces

- Required: `specs/<stable-feature-id>-<name>/plan.md` from the
  [installed plan template](../../templates/spec-kit/plan.md).
- Conditional: `research.md`, `data-model.md`, `contracts/`, and
  `quickstart.md` only when a concrete unknown, data lifecycle, formal interface,
  or end-to-end validation need justifies that artifact.

Do not emit empty or generic conditional artifacts.

## Completion

The plan is ready when project gates are checked, technical unknowns that block
design are resolved, concrete repository paths and owners are named,
compatibility and rollback boundaries are explicit, interface contracts and
dependencies agree, and planned tests cover the critical success and failure
flows. Recheck gates after design decisions.

## Next phase

`architecture-modeling`

## Supporting skills

- `dispatching-parallel-agents` for demonstrably independent read-only research.
- `verification-before-completion` for fresh artifact and gate evidence.

## Planning boundary

This phase must not edit application code. It may create only the declared
feature planning artifacts, then must return control to the coordinator. When
the original request authorizes end-to-end build work, the coordinator must
continue the declared next phase without a new request unless a material
decision, blocker, or authority boundary requires user input.

## Workflow

1. Re-read the specification and current repository; do not rely on conversation
   copies.
2. Extract constraints, component boundaries, data ownership, integrations, and
   unknowns.
3. Research only unknowns that affect a decision. Record decision, evidence,
   rationale, and considered alternatives.
4. Define the smallest sufficient architecture, compatibility strategy,
   contracts, test approach, and rollback path.
5. Create only justified supporting artifacts and link rather than duplicate
   their detail.
6. Verify the plan against the spec and applicable project gates.
