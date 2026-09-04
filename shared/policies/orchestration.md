# Orchestration

`orchestrated-implementation` is the only executor for an approved Spec Kit
`tasks.md`. The coordinator retains the specification, architecture,
cross-slice state, interface rulings, integration, and acceptance decision.

## Cohesive slices

- Group adjacent tiny tasks only when they have the same shape and one
  independently verifiable outcome.
- Keep tasks that create or consume the same interface serial and under one
  owner until that interface is stable.
- Parallel writes require disjoint path and interface ownership, isolated
  mutable state, host-provided safe isolation, an integration order, and named
  acceptance evidence. Otherwise serialize writes.
- Subagents own only the paths and report named by their slice brief. They do
  not update canonical run state, specifications, plans, shared decisions, or
  another agent's report.

## Review depth

A coordinator may review a fully specified mechanical slice. Security,
migration, interface, concurrency, data-integrity, and cross-component slices
require an independent reviewer. The complete slice range—from its recorded
base through its current head—is reviewed, including all fix commits.

## Integration

Worker summaries are claims, not acceptance evidence. The coordinator checks
reports and complete diffs, reconciles interface assumptions, integrates in the
recorded order, and runs tests proportional to the combined risk. Actionable
findings follow the defect-convergence policy and are never silently discarded.
