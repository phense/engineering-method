---
name: openspec-apply
description: "Use when an existing change under openspec/changes has complete proposal, design, delta requirements, and tasks ready for implementation. Not for proposing, archiving, defect diagnosis, or escalated work."
---

# OpenSpec Apply

Implement one approved bounded change task by task. This is the sole Brownfield
executor and the only OpenSpec phase that edits application code.

## Recovery preamble

Before implementation:

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

Use when one unambiguous active change has a complete proposal, design, delta
specification, and executable tasks, and the user authorizes implementation or
continuation of that change.

## Do not use for

- A change whose `escalation.md` contains `status: escalated`; its executor is
  inactive and work belongs to the recorded Spec Kit feature.
- Diagnosing an unexplained failure before root cause is established.
- Creating proposal artifacts or archiving completed work.

## Consumes

- `openspec/changes/<change-id>/proposal.md`
- `openspec/changes/<change-id>/design.md`
- `openspec/changes/<change-id>/tasks.md`
- `openspec/changes/<change-id>/specs/<capability>/spec.md`
- Current project gates, code, tests, and validated run state.

## Produces

- Minimal application-code and test changes required by each pending task.
- Checked task items only after their complete specified behavior and required
  verification exist.
- A conditional `escalation.md` when implementation evidence crosses the formal
  escalation boundary before further application-code edits.

## Completion

Every task is checked, no specified behavior is narrowed, deferred, or replaced,
all acceptance and compatibility criteria are implemented, and fresh targeted
verification passes. If any task is unclear or blocked, record the evidence and
pause without marking it complete.

## Next phase

`openspec-archive`

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `test-driven-development` for each meaningful testable behavior change.
- `systematic-debugging` for an observed implementation failure.
- `requesting-code-review` for risk-proportionate review.
- `verification-before-completion` for fresh evidence before task completion.

## Implementation loop

1. Re-read every planning artifact and select the first dependency-ready task.
2. State the behavior and evidence that will satisfy the task.
3. Apply `test-driven-development` where a meaningful behavior test can fail.
4. Make the smallest code change that fully implements the task.
5. Run targeted verification and review the complete task diff.
6. Mark the item complete only after its behavior and evidence are complete.
7. Continue until all tasks complete or a concrete blocker requires a pause.

If implementation reveals new-subsystem, architecture, risky-migration, or
tightly coupled cross-component scope, stop application-code edits. Write the
formal escalation record with completed task IDs and root evidence, preserve the
change path, mark `openspec-apply` inactive, and hand the traceable change to
`speckit-specify`.
