---
name: systematic-debugging
description: "Use when an observed failure, test regression, build break, performance problem, or unexplained behavior needs diagnosis before repair. Not for a deliberate behavior change with no defect evidence."
---

# Systematic Debugging

Find and demonstrate the root cause before proposing a repair. Treat each failed
hypothesis as new evidence, not permission to stack speculative fixes.

## Recovery preamble

Before continuing an investigation:

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
9. Continue from the validated next action or last evidence-backed hypothesis.

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

Use for an observed technical failure: a repeatable bug, test regression, build
or integration break, performance regression, or unexplained behavior. Capture
the exact symptom before diagnosis.

## Do not use for

- A desired intentional behavior change with no evidence that current behavior
  is defective; use `openspec-propose` or `speckit-specify` by scope.
- General code improvement without a failing or unexplained outcome.
- Implementing a known, already-approved feature task.

## Consumes

- Exact failure output, reproduction steps, and expected behavior.
- Current code, tests, configuration, environment facts, and recent changes.
- Relevant project gates and known working examples.

## Produces

- A minimal reliable reproduction, or a precise record of why reproduction is
  intermittent and what evidence is still needed.
- Boundary evidence locating the failing component and tracing the bad state to
  its source.
- One explicit root-cause hypothesis with a smallest test that can disprove it.
- A confirmed repair scope ready for test-first implementation.

## Completion

Diagnosis is complete only when the failure is reproduced, relevant component
boundaries are evidenced, differences from a working path are understood, and
the root-cause hypothesis survives its smallest test. Do not propose a fix while
the evidence identifies only a symptom or correlation.

## Next phase

`test-driven-development`

## Supporting skills

- `project-backlog` for recovery, canonical task state, events, and checkpoints.
- `dispatching-parallel-agents` only after evidence establishes independent
  failure domains.
- `verification-before-completion` for claims about reproduction or diagnosis.

## Investigation loop

1. Read the complete error, logs, stack, and failing assertion.
2. Reproduce consistently. When intermittent, vary one observable condition at
   a time and record results.
3. Review the smallest relevant recent diff and find a comparable working path.
4. At each component boundary, observe inputs, outputs, configuration, and state
   propagation. Do not log secrets or sensitive values.
5. Trace the wrong value or transition backward until its origin is explained.
6. State one hypothesis as cause and evidence. Test the smallest distinguishing
   prediction without combining repairs.
7. If disproved, discard it and form a new hypothesis from the new evidence.

After two ineffective repair attempts, obtain a fresh review of the evidence.
After three, stop local patching and examine the architecture or interface
assumption before another attempt.

## Lifecycle reclassification

A failed repair does not by itself justify a feature lifecycle. Reclassify only
when evidence establishes that the requested result is an intentional contract
change or architecture change:

Before the destination lifecycle becomes active, mark
`systematic-debugging` inactive and link the reproduction, root-cause evidence,
and stable work identity from the destination artifact.

- A bounded intentional contract change hands to `openspec-propose` with the
  reproduction and root-cause evidence.
- A new subsystem, risky migration, cross-component architecture change, or
  material architectural uncertainty hands to `speckit-specify` with the same
  evidence.
