---
name: speckit-converge
description: "Use when a Spec Kit feature has been implemented and current code, as-built architecture, integration results, review state, and fresh verification must be reconciled. Not for implementing fixes or changing approved intent."
---

# Spec Kit Converge

Compare current implementation evidence with approved feature intent. Record
every remaining actionable gap as append-only work; never become a second
implementation executor.

## Recovery preamble

Before assessing or appending an artifact:

1. Obtain host-observed live agent IDs through the platform capability seam. If
   the host cannot observe agent state, stop before mutation.
2. Invoke `project-backlog` to discover an active run and pass the observation
   explicitly to `continuity-state recover --live-agents`. Use an explicit
   empty observation only when the host confirms none are live; never omit it.
3. Complete recovery, or verify that no run exists, before any canonical or
   backlog mutation.
4. Read the run's `state.json` and `resume.md`.
5. Check recorded commits, worktree, artifacts, and canonical backlog or issue
   state against current reality.
6. Reconcile saved agent identities with agents still available from the host.
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

Use after `orchestrated-implementation` when the implementation, as-built UML,
system integration results, review state, and fresh verification evidence exist
for the current Spec Kit feature.

## Do not use for

- Implementing or fixing application code.
- Rewriting approved requirements or the technical plan.
- Reviewing an incomplete task generation artifact before implementation.

## Consumes

- Current application code and tests.
- `specs/<stable-feature-id>-<name>/spec.md`.
- `specs/<stable-feature-id>-<name>/plan.md`.
- `specs/<stable-feature-id>-<name>/tasks.md`.
- As-built UML, integration-test results, resolved and open review findings, and
  fresh verification output.

## Produces

A convergence findings summary. When actionable findings exist, append one new
numbered Convergence section with stable traceable task IDs grouped under
`### Slice <unique-slice-id>: <outcome>` headings to
`specs/<stable-feature-id>-<name>/tasks.md`. When none exist, leave `tasks.md`
byte-for-byte unchanged.

## Completion

Completion is refused while any actionable requirement, architecture,
integration, review, or verification finding remains. Convergence is complete
only when every approved requirement and plan decision is evidenced in current
code, as-built architecture agrees or records an approved rationale, integration
flows pass, review findings are resolved, and fresh verification passes.

## Next phase

`verification-before-completion`, and only after the completion condition is
met. If tasks were appended, return explicitly to the existing
`orchestrated-implementation` executor for the new slices. Preserve completed
slices, checkpoint the pending slice IDs and exact next action, and repeat
as-built reconciliation, integration verification, and convergence after the
fixes. No final handoff occurs while findings remain.

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `requesting-code-review` for risk-proportionate independent review evidence.
- `verification-before-completion` for fresh command output.

## Read-only boundary

Convergence is read-only for application code, specifications, plans, diagrams,
and existing task content. Its only allowed write is appending missing work to
`tasks.md`. Never reorder, renumber, edit, or delete an existing task.

## Workflow

1. Re-read all consumed artifacts and bound the code inspection to their paths,
   requirements, interfaces, and architecture.
2. Build an intent inventory with stable requirement and plan references.
3. Classify evidence-backed gaps as missing, partial, contradictory, or
   unrequested; assign severity by user and architecture impact.
4. Present the findings before writing.
5. Append one task per actionable finding, preserving traceability and ordering
   critical or high-severity work first. Group the new tasks into extractable
   `### Slice <unique-slice-id>: <outcome>` sections with dependencies, owned
   paths, and verification evidence. Choose task and slice IDs unused anywhere
   in the existing artifact; preserve all existing IDs and content.
6. If no actionable findings exist, do not modify any file and report the
   evidence checked.
