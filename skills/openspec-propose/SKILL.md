---
name: openspec-propose
description: "Use when a bounded intentional change to an existing capability needs delta requirements and implementation tasks. Not for a defect, new subsystem, architecture change, risky migration, or tightly coupled multi-component work."
---

# OpenSpec Propose

Describe a contained Brownfield change as a delta from current behavior and
produce the complete planning set needed by its one executor.

## Recovery preamble

Before creating or updating an artifact:

1. Invoke `project-backlog` to discover an active run relevant to this work.
2. Read its `state.json` and `resume.md`.
3. Check recorded commits, worktree, artifacts, and canonical backlog or issue
   state against current reality.
4. Reconcile saved agent identities with agents still available from the host.
5. Preserve validated completed work and never redispatch completed work after
   compaction or resumption.
6. Reconstruct stale state from git and canonical artifacts when they disagree.
7. Continue from the validated next action.

Repository evidence wins over stale checkpoint or memory data. Never silently
restart or reclassify an active workflow.

## Operational state handoffs

Invoke `project-backlog` to update backlog state and the run checkpoint at work
start, scope change, blocker discovery, each completed slice, and every phase or
final handoff. Record only concise recovery facts and the exact next action.

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
  `openspec/specs/<capability>/spec.md` when it exists.
- Any existing active change with the same stable change ID.

## Produces

Create one kebab-case `<change-id>` directory containing:

- `openspec/changes/<change-id>/proposal.md`
- `openspec/changes/<change-id>/design.md`
- `openspec/changes/<change-id>/tasks.md`
- `openspec/changes/<change-id>/specs/<capability>/spec.md`

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
2. Create `openspec/changes/<change-id>/escalation.md` from the
   [installed escalation template](../../templates/openspec/escalation.md).
3. Mark `openspec-propose` inactive, preserve the entire change directory, and
   record `status: escalated`, the evidence-backed reason, and the new Spec Kit
   feature ID and path.
4. Do not enter `openspec-apply`; begin `speckit-specify` from the recorded
   handoff.
