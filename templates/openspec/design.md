# Change Design: <change name>

## Context

<Current implementation evidence, constraints, and bounded change intent.>

## Interface contracts

| Boundary | Existing contract | Delta | Failure behavior |
|---|---|---|---|
| <component or API> | <current behavior> | <bounded change> | <handling> |

## Dependencies

| Dependency | Required change | Ordering or compatibility constraint |
|---|---|---|
| <component or service> | <change or none> | <constraint> |

## Tests

- Regression or characterization: <what current behavior is protected>
- Changed behavior: <failing test to write first>
- Compatibility: <consumer or data boundary proof>
- Targeted verification: <command or harness>

## Decisions

| Decision | Evidence | Alternative rejected |
|---|---|---|
| <bounded design choice> | <repository evidence> | <reason> |

## Risks and rollback

- <risk, mitigation, and recovery path>
