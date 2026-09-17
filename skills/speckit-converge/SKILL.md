---
name: speckit-converge
description: "Use when a Spec Kit feature has been implemented and current code, as-built architecture, integration results, review state, and fresh verification must be reconciled. Not for implementing fixes or changing approved intent."
---

# Spec Kit Converge

Apply the shared [proportionality rule](../../shared/policies/proportionality.md)
before adding work, delegating, or repeating verification.

Compare current implementation evidence with approved feature intent. Record
every remaining actionable gap as append-only work; never become a second
implementation executor.

## Recovery preamble

Before assessing or appending an artifact:

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

Use after `orchestrated-implementation` when the implementation, as-built UML,
system integration results, review state, and fresh verification evidence exist
for the current Spec Kit feature.

## Do not use for

- Implementing or fixing application code.
- Rewriting approved requirements or the technical plan.
- Reviewing an incomplete task generation artifact before implementation.

## Consumes

- Current application code and tests.
- `docs/specs/<stable-feature-id>-<name>/spec.md`.
- `docs/specs/<stable-feature-id>-<name>/plan.md`.
- `docs/specs/<stable-feature-id>-<name>/tasks.md`.
- As-built UML, integration-test results, resolved and open review findings, and
  fresh verification output.

## Produces

A convergence findings summary. When actionable findings exist, append one new
numbered Convergence section with stable traceable task IDs grouped under
`### Slice <unique-slice-id>: <outcome>` headings to
`docs/specs/<stable-feature-id>-<name>/tasks.md`. When none exist, leave `tasks.md`
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

## Playbook obligations

Apply the [playbook policy](../../shared/policies/playbooks.md): reconcile every
required development and system playbook with spec/plan/tasks, current procedures,
content review and agreed rehearsal evidence. A missing or affected content
review becomes a `playbook-review` task for the existing executor; do not invoke
a report-writing reviewer inside this read-only gate. A Ready review alone is
not execution evidence.
Missing or stale required proof is an actionable finding and prevents completion.
Append fixes/rehearsals to the existing executor's slices; never author, execute
or waive them inside convergence. Preserve system-delivery obligations when
one canonical procedure also served development.
