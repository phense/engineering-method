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

- [ ] T001 [AF-001] <resolve architecture finding before dependent implementation> — files: <paths>; evidence: <verification>

## Tests

- [ ] T002 [US-001] <write and observe a meaningful failing test> — files: <paths>; catches: <realistic break>

## Implementation slices

### Slice S1: <independently verifiable outcome>

- [ ] T003 [US-001] <focused implementation action> — files: <paths>; depends on: T001, T002
- [ ] T004 [US-001] <targeted verification and review> — evidence: <commands and review>

## Dependencies

| Work ID | Depends on | Reason | Parallel-safe with |
|---|---|---|---|
| T003 | T001, T002 | <ordering constraint> | <IDs or none> |

## Final integration

- [ ] T005 Reconcile as-built architecture with the plan and record differences.
- [ ] T006 Exercise the critical cross-component success and failure flows.
- [ ] T007 Run convergence, resolve every actionable finding, and capture fresh verification.
