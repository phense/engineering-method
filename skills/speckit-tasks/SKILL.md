---
name: speckit-tasks
description: Use when a Spec Kit plan.md and its design or architecture findings are complete and need dependency-ordered implementation tasks. Not for implementation or an unplanned feature.
---

# Spec Kit Tasks

Convert an approved plan and architecture findings into stable,
dependency-ordered tasks grouped as cohesive implementation slices.

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
