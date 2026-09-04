---
name: speckit-tasks
description: Use when a Spec Kit plan.md and its design or architecture findings are complete and need dependency-ordered implementation tasks. Not for implementation or an unplanned feature.
---

# Spec Kit Tasks

Convert an approved plan and architecture findings into stable,
dependency-ordered tasks grouped as cohesive implementation slices.

## Recovery preamble

Before creating or updating an artifact:

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

Use when `spec.md`, `plan.md`, and required design-time architecture findings
exist for a Spec Kit feature and `tasks.md` is absent or needs regeneration
before implementation starts.

## Do not use for

- Work without an approved Spec Kit plan.
- Implementing generated tasks.
- An active OpenSpec change or a standalone defect.

## Consumes

- `specs/<stable-feature-id>-<name>/spec.md`.
- `specs/<stable-feature-id>-<name>/plan.md`.
- Justified `research.md`, `data-model.md`, `contracts/`, and `quickstart.md`
  artifacts when present.
- Design-time UML evidence and every open architecture finding.

## Produces

`specs/<stable-feature-id>-<name>/tasks.md` from
the [installed tasks template](../../templates/spec-kit/tasks.md), with
immutable sequential task IDs, explicit
paths, source requirement or finding references, dependency edges, and
verification evidence.

## Completion

Every acceptance criterion, interface contract, test obligation, architecture
finding, migration or rollback need, and integration flow maps to at least one
task. Tasks are ordered by dependency, grouped into independently verifiable
cohesive slices, and marked parallel-safe only when file ownership and
dependencies are disjoint.

## Next phase

`orchestrated-implementation`

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `verification-before-completion` for task coverage and format checks.

## Planning boundary

This phase must not edit application code. It creates or repairs the task
artifact only, then must return control to the coordinator. When the original
request authorizes end-to-end build work, the coordinator must continue the
declared next phase without a new request unless a material decision, blocker,
or authority boundary requires user input.

## Workflow

1. Re-read all input artifacts from disk and build a traceability inventory.
2. Convert architecture findings into tasks before any dependent implementation.
3. Add meaningful test-first tasks before the behavior they protect.
4. Group setup and shared prerequisites only when they truly block multiple
   outcomes; organize remaining work by independently valuable slice.
5. Give every task an exact action, path, dependency, and acceptance evidence.
6. Validate coverage, ordering, stable IDs, and safe parallel markers.
