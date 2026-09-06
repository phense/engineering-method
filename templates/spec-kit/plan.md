# Implementation Plan: <feature name>

## Stable work ID

- Feature ID: `<stable-feature-id>`
- Specification: `docs/specs/<stable-feature-id>-<name>/spec.md`
- Artifact path: `docs/specs/<stable-feature-id>-<name>/plan.md`

## Summary

<Primary requirement and evidence-backed technical approach.>

## Project gates

| Gate | Evidence | Result |
|---|---|---|
| <applicable repository rule> | <path or command> | <pass, conflict, or follow-up> |

## Technical context

- Languages and versions: <current versions>
- Relevant components and paths: <real repository paths>
- Storage and external systems: <systems or not applicable>
- Constraints and scale: <constraints>

## Compatibility boundaries

- Preserved behavior: <behavior>
- Migration and rollback: <strategy>
- Deployment or versioning boundary: <boundary>

## Interface contracts

| Contract ID | Producer | Consumer | Contract change | Failure behavior |
|---|---|---|---|---|
| IC-001 | <producer> | <consumer> | <change or preserved contract> | <handling> |

## Dependencies

| Dependency | Why needed | Availability or ordering |
|---|---|---|
| <component, decision, or external system> | <reason> | <constraint> |

## Tests

- Targeted: <behavior and command or harness>
- Contract: <interface proof>
- Integration: <cross-component success and failure flows>
- Migration or rollback: <proof or not applicable>

## Architecture findings

| Finding ID | Evidence | Required response | Status |
|---|---|---|---|
| AF-001 | <diagram, code, or contract> | <task-worthy action> | Open |

## Supporting artifacts

Create only artifacts justified by current risk or uncertainty:

- `research.md`: <specific unresolved technical question, or omit>
- `data-model.md`: <changed data ownership or lifecycle, or omit>
- `contracts/`: <formal interface details, or omit>
- `quickstart.md`: <integration validation procedure, or omit>

## Implementation structure

<Concrete repository paths and component ownership.>
