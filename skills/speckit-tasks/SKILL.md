---
name: speckit-tasks
description: Use when a Spec Kit plan.md and its design or architecture findings are complete and need dependency-ordered implementation tasks. Not for implementation or an unplanned feature.
---

# Spec Kit Tasks

Convert an approved plan and architecture findings into stable,
dependency-ordered tasks grouped as cohesive implementation slices.

## Recovery preamble

Before creating or updating an artifact:

1. Look for a relevant `.engineering-method/runs/<work-id>/state.json` and
   `resume.md`.
2. Compare recorded commits, worktree, artifacts, and canonical task state with
   the repository.
3. Repository evidence wins over stale checkpoint or memory data.
4. Preserve validated completed work and never redispatch completed work after
   compaction or resumption.
5. Continue the recorded next action when it still matches current evidence;
   otherwise reconstruct the phase from git and canonical artifacts.

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
`templates/spec-kit/tasks.md`, with immutable sequential task IDs, explicit
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
artifact only and never starts implementation in the same phase.

## Workflow

1. Re-read all input artifacts from disk and build a traceability inventory.
2. Convert architecture findings into tasks before any dependent implementation.
3. Add meaningful test-first tasks before the behavior they protect.
4. Group setup and shared prerequisites only when they truly block multiple
   outcomes; organize remaining work by independently valuable slice.
5. Give every task an exact action, path, dependency, and acceptance evidence.
6. Validate coverage, ordering, stable IDs, and safe parallel markers.
