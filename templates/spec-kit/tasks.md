# Tasks: <feature name>

## Stable work ID

- Feature ID: `<stable-feature-id>`
- Specification: `specs/<stable-feature-id>-<name>/spec.md`
- Plan: `specs/<stable-feature-id>-<name>/plan.md`
- Artifact path: `specs/<stable-feature-id>-<name>/tasks.md`

Use stable task IDs. Order blockers before their dependents and group work into
cohesive, independently verifiable slices. Mark `[P]` only when ownership and
dependencies allow safe parallel work.

## Architecture findings

Record finding IDs, affected interfaces, ownership, and required resolution.
Place each actionable response in an implementation slice below.

## Tests

Record the behavior each test must catch and the relevant commands. Keep each
red test with its implementation and green verification in one cohesive slice.

## Implementation slices

### Slice S1: <independently verifiable outcome>

- [ ] T001 [AF-001] <analyze the finding and settle ownership and interfaces without changing code> — files: <paths>; evidence: <analysis>
- [ ] T002 [US-001] [AF-001] <write and observe a meaningful failing test> — files: <paths>; catches: <realistic break>; depends on: T001
- [ ] T003 [US-001] [AF-001] <implement the outcome and resolve the architecture finding> — files: <paths>; depends on: T001, T002
- [ ] T004 [US-001] <targeted verification and review> — evidence: <commands and review>

## Dependencies

| Work ID | Depends on | Reason | Parallel-safe with |
|---|---|---|---|
| T003 | T001, T002 | <ordering constraint> | <IDs or none> |

## Final integration

### Slice S2: Reconcile and verify integrated behavior

Coordinator-owned integration gate after all implementation slices pass.

- [ ] T005 Reconcile as-built architecture with the plan and record differences.
- [ ] T006 Exercise the critical cross-component success and failure flows.

### Slice S3: Convergence and final verification handoff

Coordinator-owned phase handoff. Invoke `speckit-converge` for assessment;
route any appended fix slices back through the existing
`orchestrated-implementation` executor before final verification.

- [ ] T007 Run convergence, resolve every actionable finding, and capture fresh verification.
