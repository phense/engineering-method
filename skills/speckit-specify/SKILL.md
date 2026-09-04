---
name: speckit-specify
description: "Use when a new capability, cross-component feature, architecture change, risky migration, or material unresolved design needs specification. Not for a reproducible defect or bounded Brownfield delta."
---

# Spec Kit Specify

Turn a large or architecture-bearing outcome into one technology-neutral,
testable feature specification. This phase owns requirements, not design or
implementation.

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

Use for a new capability, tightly coupled cross-component feature, system
boundary or architecture change, risky migration, or materially unresolved
design. If an existing feature has a complete spec, continue with its recorded
next phase instead of specifying it again.

## Do not use for

- A reproducible defect or unexplained failure; use `systematic-debugging`.
- A bounded intentional change to one existing capability; use
  `openspec-propose`.
- A small reversible edit with no behavior-contract impact.

## Consumes

- The requested user outcome and explicit constraints.
- Applicable project gates and protected controls.
- Current repository, tests, interfaces, and nearby documentation.
- Any validated active-run state for the stable work ID.

## Produces

Create or update exactly
`specs/<stable-feature-id>-<name>/spec.md` from
the [installed specification template](../../templates/spec-kit/spec.md).
Preserve an existing stable feature ID; otherwise
derive an immutable project-conventional ID and record the source request.

## Completion

The specification is ready when it contains prioritized independently testable
user outcomes, measurable acceptance criteria, explicit scope and compatibility
boundaries, interface contracts, edge cases, assumptions, and no unresolved
ambiguity that would materially change scope or observable behavior. Validate
the artifact against those criteria and report its path.

## Next phase

`speckit-plan`

## Supporting skills

- `verification-before-completion` for fresh artifact checks.

## Planning boundary

This phase must not edit application code. After verifying the artifact, return
control to the coordinator. When the original request authorizes end-to-end
build work, the coordinator must continue the declared next phase without a new
request unless a material decision, blocker, or authority boundary requires
user input.

## Workflow

1. Inspect relevant code, tests, and project rules proportionally to the feature.
2. Choose a concise stable directory name independently of branch naming.
3. Separate user needs and observable outcomes from implementation choices.
4. Make reasonable defaults explicit. Ask before writing when ambiguity would
   materially alter scope, security, compatibility, or acceptance.
5. Fill the template with concrete content; remove unused example rows.
6. Review every requirement for testability and every acceptance criterion for
   technology-neutral observability.
