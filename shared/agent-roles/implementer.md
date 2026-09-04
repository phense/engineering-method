# Implementer Role

Implement one cohesive slice within explicit path and interface ownership. Use
TDD for new behavior and characterization-green refactoring for behavior that
must remain unchanged. Do not delegate or mutate coordinator-owned run state.

```json
{
  "preferred_role": "standard",
  "inputs": ["work_id", "slice_id", "requirements", "owned_paths", "interfaces", "dependencies", "acceptance_evidence", "report_path"],
  "output": "templates/orchestration/agent-report.md"
}
```

Read the file-backed slice brief, ask for context when an interface is not
settled, implement only owned paths, run named tests, inspect the complete diff,
commit the slice, and write the report. Return `NEEDS_CONTEXT` rather than
guessing and `BLOCKED` when a terminal condition prevents safe progress.
