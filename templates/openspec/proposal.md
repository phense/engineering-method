# Change Proposal: <change name>

## Stable work ID

- Change ID: `<change-id>`
- Artifact path: `docs/openspec/changes/<change-id>/proposal.md`
- Status: Proposed

## Why

<Observed need and why a bounded delta is appropriate.>

## Changed requirements

List added, modified, removed, or renamed requirements under
`docs/openspec/changes/<change-id>/specs/<capability>/spec.md`. Describe only the
delta to the existing capability.

## Acceptance criteria

- AC-001 — Given <existing state>, when <changed behavior>, then <observable result>.
- AC-002 — Given <boundary or failure>, when <changed behavior>, then <compatible result>.

## Compatibility boundaries

- Existing behavior preserved: <behavior>
- Consumers, data, and versions affected: <boundaries>
- Migration and rollback: <expectations or not applicable>

## Scope

- In scope: <bounded change>
- Out of scope: <new subsystems, architecture work, or unrelated behavior>

## Escalation check

- New subsystem: No
- Tightly coupled multi-component reach: No
- Risky migration: No
- Material architecture uncertainty: No

If any answer becomes Yes, stop OpenSpec execution and create `escalation.md`.
