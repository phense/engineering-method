---
name: speckit-plan
description: "Use when an existing Spec Kit spec.md is complete and needs an evidence-grounded technical plan. Not for writing requirements, implementing code, or planning a bounded OpenSpec change."
---

# Spec Kit Plan

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Translate an approved feature specification into an evidence-grounded technical
plan while keeping requirements and implementation separate.

## Recovery preamble

Before creating or updating an artifact:

1. Invoke `project-backlog` for read-only discovery: discover an active run
   for the stable work ID before requesting agent status. Only a verified absent
   run may enroll in the new-run-only coordinator-only mode described there.
2. For an existing ordinary run, obtain host-observed live agent IDs through
   the platform capability seam and call `continuity-state recover --live-agents`.
   Use an explicit empty observation only when the host confirms none are live.
   With no observation, only verified coordinator-only provenance permits
   `continuity-state recover --coordinator-only`; saved or uncertain agent
   activity remains blocked. Never fabricate observed IDs.
3. Complete recovery, or verified absent-run initialization, before any canonical
   or backlog mutation. The coordinator-only mode permits sequential continuity
   across phase handoffs, not delegation or bypass of independent-review gates.
4. Read the run's `state.json` and `resume.md` when a run exists.
5. Check recorded commits, worktree, artifacts, and canonical backlog or issue
   state against current reality.
6. Reconcile saved agent identities with agents still available from the host;
   coordinator-only recovery must verify that no saved agent history exists.
7. Preserve validated completed work and never redispatch completed work after
   compaction or resumption.
8. Reconstruct stale state from git and canonical artifacts when they disagree.
9. Continue from the validated next action.

Repository evidence wins over stale checkpoint or memory data. Never silently
restart or reclassify an active workflow.

## Operational state handoffs

Follow the [transition-to-event ordering
contract](../project-backlog/SKILL.md#transition-to-event-ordering):

1. After each durable transition, invoke `project-backlog` to call
   `continuity-state event` with the applicable event and its concise facts.
2. Then call `continuity-state checkpoint` with current state and the exact next
   action, except where the dispatch or completion protocol requires two
   checkpoints.
3. Event emission is never automatic. Claim it only after the event call
   succeeds, and likewise verify every checkpoint call.

Apply this protocol while updating backlog state and the run checkpoint at work
start, scope change, blocker discovery, each completed slice, and every phase or
final handoff.

## Trigger

Use when `docs/specs/<stable-feature-id>-<name>/spec.md` exists, satisfies its
acceptance contract, and has no current `plan.md`, or when repository evidence
requires that plan to be updated before architecture analysis.

## Do not use for

- Creating or clarifying feature requirements; use `speckit-specify`.
- Implementing any plan or task.
- A bounded existing-capability delta owned by OpenSpec.

## Consumes

- `docs/specs/<stable-feature-id>-<name>/spec.md`.
- Applicable project gates, repository structure, code, tests, and interfaces.
- Existing validated research or design evidence for the same feature.

## Produces

- Required: `docs/specs/<stable-feature-id>-<name>/plan.md` from the
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

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
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

## Playbook obligations

Apply the [playbook policy](../../shared/policies/playbooks.md). Assess critical
**development** operations independently of the specified **system** deliverables.
Record IDs, canonical paths, owners, operation/delivery dependencies, readiness
deadlines and proportionate review/rehearsal criteria in the plan. Record none
with rationale when appropriate. Feed new delivery scope back to the specification
owner; do not silently add or drop requirements.
