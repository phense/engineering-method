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
numbered Convergence section with stable traceable task IDs to
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
met. If tasks were appended, the lifecycle remains in implementation and no
handoff occurs.

## Supporting skills

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
   critical or high-severity work first.
6. If no actionable findings exist, do not modify any file and report the
   evidence checked.
