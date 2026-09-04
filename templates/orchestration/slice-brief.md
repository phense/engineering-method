# Slice Brief

```json
{
  "purpose": "dispatch",
  "required": ["work_id", "slice_id", "requirements", "owned_paths", "forbidden_paths", "interfaces", "dependencies", "base_commit", "acceptance_evidence", "report_path"]
}
```

## Identity

- Work ID: `<work-id>`
- Slice ID: `<slice-id>`
- Base commit: `<full-commit>`
- Requested capability role: `<strong-standard-or-fast>`
- Report path: `.engineering-method/runs/<work-id>/agent-reports/<agent-id>.md`

## Requirements and evidence

List stable requirement and task IDs, the independently verifiable outcome,
the targeted commands, and the literal expected behavior.

## Ownership and interfaces

List owned paths, forbidden paths, interface contracts, dependencies, and any
facts that must remain stable. State whether writes are serialized or safely
isolated.

## Handoff

Name the commit, files, test evidence, root-cause or fix findings, concerns, and
next dependency facts the report must return.
