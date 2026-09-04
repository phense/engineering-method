# Lifecycle Handoffs

Every phase consumes current artifacts from disk, creates or updates only its
declared outputs, verifies its completion condition, and names one next phase.
Semantic skill names are portable; platform adapters decide how to invoke them.

The following JSON is the authoritative, machine-readable handoff graph:

```json
{
  "nodes": [
    "systematic-debugging",
    "test-driven-development",
    "verification-before-completion",
    "openspec-propose",
    "openspec-apply",
    "openspec-archive",
    "speckit-specify",
    "speckit-plan",
    "architecture-modeling",
    "speckit-tasks",
    "orchestrated-implementation",
    "speckit-converge"
  ],
  "executors": {
    "bugfix": "test-driven-development",
    "openspec": "openspec-apply",
    "speckit": "orchestrated-implementation"
  },
  "edges": [
    {"from": "systematic-debugging", "to": "test-driven-development", "artifact": "reproduction and root-cause evidence"},
    {"from": "test-driven-development", "to": "verification-before-completion", "artifact": "verified red-green evidence"},
    {"from": "openspec-propose", "to": "openspec-apply", "artifact": "openspec/changes/<change-id>/tasks.md"},
    {"from": "openspec-apply", "to": "openspec-archive", "artifact": "completed tasks and fresh verification"},
    {"from": "speckit-specify", "to": "speckit-plan", "artifact": "specs/<stable-feature-id>-<name>/spec.md"},
    {"from": "speckit-plan", "to": "architecture-modeling", "artifact": "specs/<stable-feature-id>-<name>/plan.md"},
    {"from": "architecture-modeling", "to": "speckit-tasks", "artifact": "verified design findings"},
    {"from": "speckit-tasks", "to": "orchestrated-implementation", "artifact": "specs/<stable-feature-id>-<name>/tasks.md"},
    {"from": "orchestrated-implementation", "to": "speckit-converge", "artifact": "implementation, as-built models, integration results, and review state"},
    {"from": "speckit-converge", "to": "verification-before-completion", "artifact": "closed or appended convergence findings"},
    {"from": "openspec-propose", "to": "speckit-specify", "artifact": "openspec/changes/<change-id>/escalation.md", "condition": "status: escalated"}
  ]
}
```

The escalation edge is exceptional: preserve the OpenSpec change, write the
formal escalation record, and make its executor inactive before Spec Kit starts.
