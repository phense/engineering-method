<!--
Authoring contract:
- Keep only the operations used by this delta; at least one operation is required.
- The exact text after `### Requirement:` is the stable requirement identity.
  Preserve it for ADDED, MODIFIED, and REMOVED. Use RENAMED for identity changes.
- Every ADDED or MODIFIED requirement has normative SHALL or MUST text and at
  least one scenario.
- A scenario heading uses exactly four hash marks and a stable scenario name,
  followed by WHEN and THEN bullets that describe observable behavior.
- A MODIFIED requirement is a complete replacement block copied from the current
  main spec and edited. It includes every surviving scenario; omitted scenarios
  are removed, so partial modification is invalid.
- A REMOVED requirement includes Reason and Migration.
- A RENAMED entry changes identity only. Put behavior changes under MODIFIED using
  the TO identity.

Merge contract:
- Reject duplicate identities and any conflict between operation sections.
- For an existing main spec, merge RENAMED then REMOVED then MODIFIED then ADDED.
- If the main spec does not exist, only ADDED requirements are valid and Purpose
  seeds the new capability. Never synthesize a target for other operations.
- The merged main spec has one `## Requirements` section and no operation headers.
-->

## Purpose

<For a new capability only, explain its purpose in one or two concrete sentences. Remove this section for an existing capability.>

## ADDED Requirements

### Requirement: <stable requirement name>

The system SHALL <new observable behavior>.

#### Scenario: <stable scenario name>

- **WHEN** <condition or action>
- **THEN** <observable outcome>

## MODIFIED Requirements

### Requirement: <exact existing or renamed-to requirement name>

The system SHALL <complete updated requirement text>.

#### Scenario: <every surviving scenario name>

- **WHEN** <condition or action>
- **THEN** <observable outcome>

## REMOVED Requirements

### Requirement: <exact existing requirement name>

- **Reason**: <why the behavior is removed>
- **Migration**: <how consumers preserve or replace their behavior>

## RENAMED Requirements

- FROM: `### Requirement: <exact existing name>`
- TO: `### Requirement: <new stable name>`
