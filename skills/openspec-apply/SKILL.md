---
name: openspec-apply
description: "Use when an existing change under openspec/changes has complete proposal, design, delta requirements, and tasks ready for implementation. Not for proposing, archiving, defect diagnosis, or escalated work."
---

# OpenSpec Apply

Implement one approved bounded change task by task. This is the sole Brownfield
executor and the only OpenSpec phase that edits application code.

## Recovery preamble

Before implementation:

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
