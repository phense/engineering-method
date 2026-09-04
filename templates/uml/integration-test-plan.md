# Architecture-Derived Integration Test Plan

```json
{
  "minimum_derived_tests": {"success": 1, "recovery": 1},
  "completion_requires": ["as_built_reconciliation", "derived_success_test_passed", "derived_recovery_test_passed", "clean_final_review", "fresh_verification"]
}
```

## Inputs

- Work ID and requirement IDs: `<stable IDs>`
- Reconciled component diagram: `<repository-relative path>`
- Reconciled success sequence: `<repository-relative path>`
- Reconciled recovery sequence: `<repository-relative path>`
- Reconciled state diagram: `<repository-relative path>`
- Reconciliation evidence: `<repository-relative path>`

## Derived success test

- Test ID and path: `<stable ID and repository-relative path>`
- Diagram edges/states exercised: `<messages, boundaries, and transitions>`
- Real collaborating components: `<component names>`
- Setup and stimulus: `<controlled inputs>`
- Observable assertions: `<outputs, state, side effects, and ordering>`
- Command and result: `<exact fresh command and complete result>`

## Derived recovery test

- Test ID and path: `<stable ID and repository-relative path>`
- Failure injection: `<specific controlled failure>`
- Diagram edges/states exercised: `<failure, compensation, and terminal state>`
- Real collaborating components: `<component names>`
- Observable assertions: `<rollback, recovery, state, and ordering>`
- Command and result: `<exact fresh command and complete result>`

## Gate evidence

Record as-built reconciliation, both passing derived paths, clean final review,
and fresh verification with timestamp and artifact pointers. If any condition
is absent or failing, create an actionable finding and refuse the
`speckit-converge` completion handoff.
