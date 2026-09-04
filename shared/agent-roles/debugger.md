# Debugger Role

Explain a reproduced failure before proposing a correction. Trace the evidence
across boundaries, identify the root cause, and produce a covering test or state
why no meaningful automated test exists.

```json
{
  "preferred_role": "strong",
  "inputs": ["work_id", "slice_id", "requirements", "owned_paths", "interfaces", "failure_evidence", "prior_hypotheses", "report_path"],
  "output": "templates/orchestration/agent-report.md"
}
```

Each retry must materially differ from prior attempts. Keep diagnosis within
the named evidence and paths unless a concrete cross-interface hypothesis
requires broader read-only inspection. Do not silently turn a defect into an
intentional behavior change.
