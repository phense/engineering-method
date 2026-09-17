---
name: openspec-propose
description: "Use when a bounded intentional change to an existing capability needs delta requirements and implementation tasks. Not for a defect, new subsystem, architecture change, risky migration, or tightly coupled multi-component work."
---

# OpenSpec Propose

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Describe a contained Brownfield change as a delta from current behavior and
produce the complete planning set needed by its one executor.

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

Use for an intentional, bounded behavior change to an existing capability when
the current implementation and specification can be inspected and the delta can
remain within its established component boundaries.

## Do not use for

- An observed failure or reproducible defect; use `systematic-debugging`.
- A new subsystem or capability, architecture change, risky migration, tightly
  coupled multi-component change, or unresolved design that cannot be contained;
  use `speckit-specify` through the formal escalation path.
- A small reversible edit with no behavior-contract impact.

## Consumes

- The requested behavior delta and explicit constraints.
- Applicable project gates, current code and tests, nearby interfaces, and
  `docs/openspec/specs/<capability>/spec.md` when it exists.
- Any existing active change with the same stable change ID.

## Produces

Create one kebab-case `<change-id>` directory containing:

- `docs/openspec/changes/<change-id>/proposal.md`
- `docs/openspec/changes/<change-id>/design.md`
- `docs/openspec/changes/<change-id>/tasks.md`
- `docs/openspec/changes/<change-id>/specs/<capability>/spec.md`

Use the installed [proposal](../../templates/openspec/proposal.md),
[design](../../templates/openspec/design.md),
[tasks](../../templates/openspec/tasks.md), and
[delta-spec](../../templates/openspec/spec.md) templates. The capability spec
records only added, modified, removed, or renamed requirements and preserves the
capability's full existing path.

## Completion

The proposal is ready when the delta is acceptance-testable, compatibility and
rollback boundaries are explicit, interfaces and dependencies agree, tasks are
dependency ordered with meaningful tests, all artifacts exist, and the
escalation check remains negative.

## Next phase

`openspec-apply`

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `verification-before-completion` for fresh artifact checks.

## Planning boundary

This phase must not edit application code. After verifying the artifacts, return
control to the coordinator. When the original request authorizes end-to-end
change work, the coordinator must continue the declared next phase without a
new request unless a material decision, blocker, or authority boundary requires
user input.

## Workflow

1. Resolve one stable change ID. If that active ID already exists, continue it
   rather than overwrite it or silently create a duplicate.
2. Inspect the affected code, tests, main capability spec, and consumers.
3. Distinguish current evidence, the proposed delta, and assumptions.
4. Write proposal, delta requirements, design, and tasks in dependency order,
   re-reading each completed input from disk before using it.
5. Verify each artifact and the bounded-change criteria.

## Formal escalation

If evidence reveals a new subsystem, architecture work, a risky migration,
tightly coupled multi-component scope, or material architectural uncertainty:

1. Stop planning the Brownfield delta.
2. Create `docs/openspec/changes/<change-id>/escalation.md` from the
   [installed escalation template](../../templates/openspec/escalation.md).
3. Mark `openspec-propose` inactive, preserve the entire change directory, and
   record `status: escalated`, the evidence-backed reason, and the new Spec Kit
   feature ID and path.
4. Do not enter `openspec-apply`; begin `speckit-specify` from the recorded
   handoff.

## Playbook obligations

Apply the [playbook policy](../../shared/policies/playbooks.md) to this delta.
Record system-deliverable playbooks in proposal and delta requirements, and
critical development-operation playbooks in design. Include affected existing
procedures or a concise none/rationale. Assign IDs, owners, paths, dependencies,
deadlines and review/rehearsal criteria. Tasks must make development readiness a
prerequisite of the operation and system readiness a prerequisite of delivery.
Planned usage or recovery risk is sufficient origin evidence.
