# Orchestration Continuity Contract

Orchestration consumes the EM-002 state service; it does not define or write a
second state format. The installed `continuity-state` interface owns
`.engineering-method/runs/<work-id>/state.json`, `resume.md`, `decisions.md`,
`agent-reports/`, and `events.jsonl`.

## Ownership

- The coordinator is the sole writer of `state.json`, `resume.md`, and
  `decisions.md`, and the sole event producer for orchestration transitions.
- A subagent writes only its named file below `agent-reports/` through the
  existing EM-002 report interface.
- Git, current artifacts, tests, and canonical backlog or issue state outrank a
  stale checkpoint or recalled memory value.

## Checkpoints

Use the existing EM-002 event and checkpoint operations before and after a
dispatch, after implementation, test, review, and fix transitions, before a
long wait, after each slice, at phase transitions, and before handoff. Record
the exact next action. Event success precedes the checkpoint that records its
result, except dispatch and completion protocols that deliberately bracket the
external action with two checkpoints.

## Recovery

Recover with explicit host-observed live agent IDs. Validate the recorded
worktree, commits, artifacts, reports, and canonical work before continuing.
Preserve completed slices, keep observed active agents active, and make only
unavailable active agents redispatchable. Downstream memory may provide the
work ID and artifact pointers, but cannot override repository evidence.
