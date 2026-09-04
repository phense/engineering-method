# Change Tasks: <change name>

## Stable work ID

- Change ID: `<change-id>`
- Proposal: `openspec/changes/<change-id>/proposal.md`
- Artifact path: `openspec/changes/<change-id>/tasks.md`

Each checked item represents fully implemented behavior with its required
evidence. Keep task IDs stable when ordering changes.

## Tests

- [ ] C001 Write and observe a failing test for <changed behavior> — catches: <realistic break>

## Implementation

- [ ] C002 Implement <bounded delta> — files: <paths>; depends on: C001
- [ ] C003 Verify preserved compatibility behavior — evidence: <command or harness>

## Dependencies

| Work ID | Depends on | Reason | Parallel-safe with |
|---|---|---|---|
| C002 | C001 | Test-first implementation | <IDs or none> |

## Completion evidence

- [ ] C004 All tasks are complete with no deferred specified behavior.
- [ ] C005 Fresh targeted verification passes.
- [ ] C006 Accepted requirement deltas are ready to synchronize before archive.
