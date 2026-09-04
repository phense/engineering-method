---
name: architecture-modeling
description: "Use for design-time or as-built architecture analysis of a large cross-component feature, changed system boundary, architectural refactor, substantial migration, or cross-component concurrency, security, or data-integrity work. Not for small fixes, localized Brownfield changes, documentation, or mechanical refactors."
---

# Architecture Modeling

Create only evidence-backed models that answer named architecture questions.
This skill is original and self-contained for the engineering method.

## Recovery preamble

Before creating or reconciling an artifact:

1. Obtain host-observed live agent identities through the platform capability
   seam. If the host cannot observe agent state, stop before mutation.
2. Invoke `project-backlog` to discover the stable work ID and use the existing
   EM-002 `continuity-state recover` interface with an explicit observation,
   including an explicitly confirmed empty set.
3. Read `state.json` and `resume.md`; validate commits, worktree, specifications,
   plans, tasks, current UML, reports, and canonical backlog or issue state.
4. Preserve completed analysis and reconcile stale pointers from repository
   evidence before continuing at the recorded next action.

Repository evidence wins over checkpoint or memory values. Never silently
restart or reclassify the active lifecycle.

## Operational state handoffs

Follow the [EM-002 transition-to-event
ordering](../project-backlog/SKILL.md#transition-to-event-ordering). After each
durable finding, diagram decision, design/as-built mode transition, or blocker,
emit the applicable event and then checkpoint current artifact paths, open
findings, verification evidence, and exact next action. Checkpoint before a
long wait and at every handoff. Event and checkpoint claims require successful,
read output.

## Trigger

Use in the Spec Kit lifecycle after an approved plan and before task generation,
then again after implementation for as-built reconciliation. Current evidence
must match one category in the [architecture gate
policy](../../shared/policies/architecture-gate.md).

## Do not use for

- Small fixes or ordinary localized defects.
- Localized Brownfield changes owned by OpenSpec.
- Documentation-only changes.
- Mechanical refactors without an architecture-spanning risk.
- Producing diagrams merely for completeness.

## Consumes

- The approved Spec Kit specification and plan, including requirements and
  interface contracts.
- Current repository code, tests, deployment configuration, and project gates.
- In as-built mode, completed tasks, implementation commits, agent reports, and
  current test evidence.

## Produces

- Relevant Mermaid sources under `docs/uml/`, each with purpose, source
  evidence, requirement IDs, notation, and verification date.
- `docs/uml/findings.md` with stable IDs, evidence, required response, and
  status.
- In as-built mode, reconciled models and one disposition for every difference.

## Completion

Design-time work is complete only when every named question is answered,
required analysis checks have evidence, and all open findings exist in
`docs/uml/findings.md` before task generation. As-built work is complete only
when diagrams match current code or record a justified correction, unresolved
differences remain actionable, and the reconciliation is ready for
system-architect integration-test derivation.

## Next phase

Design-time completion hands off to `speckit-tasks`. As-built completion returns
to the owning `orchestrated-implementation` phase for system integration and
then `speckit-converge`; it does not bypass either gate.

## Supporting skills

- `project-backlog` for EM-002 recovery, events, and checkpoints.
- `verification-before-completion` for current syntax and evidence checks.
- `speckit-tasks` consumes design-time findings.
- `orchestrated-implementation` supplies as-built code and test evidence.

## Select the question before the notation

Use the [UML template guide](../../templates/uml/README.md). Write the question
first, then choose only a diagram that materially improves its answer:

| Question | Smallest useful view |
|---|---|
| Who owns each responsibility, interface, dependency, or trust boundary? | Component |
| In what order do cross-component success, failure, rollback, or concurrent messages occur? | Sequence |
| Which lifecycle states and transitions are valid, reachable, terminal, or recoverable? | State |
| How do branching work, parallel activity, or migration steps converge? | Activity |
| Which runtime boundary, zone, process, store, or network edge affects behavior? | Deployment |

Omit a view when prose or an existing model already answers the question. Do
not create a fixed diagram set for every feature.

## Notation and validation

Mermaid is the dependency-free default for repository rendering. Start from the
smallest applicable template and keep source beside its metadata. If a Mermaid
renderer is available, render the file and treat syntax errors as failed
verification. Without a renderer, inspect the diagram directive, identifiers,
relationships, block pairing, and labels; record that semantic source review
was used rather than claiming a render.

PlantUML is permitted only when it adds material modeling value that Mermaid
cannot express adequately and a validator is available. Record that decision,
the validator command, and its result. Never introduce a renderer dependency
only to satisfy this gate.

## Design-time workflow

1. Record the activation evidence and mode in the run checkpoint.
2. Inventory requirements, components, ownership, interfaces, states, critical
   flows, data, trust boundaries, deployment facts, and migration steps from
   the approved plan and repository.
3. For each unresolved architecture question, create the smallest relevant
   diagram and attach the [metadata
   contract](../../templates/uml/diagram-metadata.md).
4. Compare models with the evidence for missing or conflicting ownership,
   interface mismatches, dependency cycles, invalid or unreachable states,
   failure or rollback gaps, ordering or races, trust-boundary gaps, and
   migration consistency.
5. Write each result to `docs/uml/findings.md` before `speckit-tasks`. Use
   `AF-001`, `AF-002`, and subsequent stable IDs; include question, requirement
   IDs, diagram and repository evidence, impact, required response, and status.
6. Verify Mermaid sources and checkpoint the findings-to-task handoff.

## As-built workflow

1. Re-read implemented interfaces and critical flows from code and current
   tests; do not reconcile from agent summaries.
2. Compare each relevant design-time node, edge, message, state, and boundary
   with implementation evidence.
3. For every difference, correct code, correct the diagram with an explicit
   rationale, or record an unresolved defect. Never ignore drift because unit
   tests pass.
4. Update metadata verification dates and evidence pointers, then verify syntax
   again.
5. Complete reconciliation before a system architect derives integration tests
   from the component, success, failure/recovery, and state views.

## Findings format

Each `docs/uml/findings.md` entry contains:

- stable `AF-NNN` identity and status;
- the named question and requirement IDs;
- diagram path plus exact plan/code/test evidence;
- one analysis category and impact;
- the required task or, after implementation, difference disposition and
  rationale;
- verification date and exact next action.
