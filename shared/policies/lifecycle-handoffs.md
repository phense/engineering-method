# Lifecycle Handoffs

Every phase consumes current artifacts from disk and names one next phase.

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
    {
      "from": "systematic-debugging",
      "to": "test-driven-development",
      "artifact": "reproduction and root-cause evidence"
    },
    {
      "from": "systematic-debugging",
      "to": "openspec-propose",
      "artifact": "docs/openspec/changes/<change-id>/proposal.md",
      "condition": "evidence establishes a bounded intentional contract change",
      "deactivates": "systematic-debugging",
      "traceability": "proposal links the reproduction and root-cause evidence"
    },
    {
      "from": "systematic-debugging",
      "to": "speckit-specify",
      "artifact": "docs/specs/<stable-feature-id>-<name>/spec.md",
      "condition": "evidence establishes an architecture change or large-feature scope",
      "deactivates": "systematic-debugging",
      "traceability": "feature spec links the reproduction and root-cause evidence"
    },
    {
      "from": "test-driven-development",
      "to": "verification-before-completion",
      "artifact": "verified red-green evidence"
    },
    {
      "from": "openspec-propose",
      "to": "openspec-apply",
      "artifact": "docs/openspec/changes/<change-id>/tasks.md"
    },
    {
      "from": "openspec-apply",
      "to": "openspec-archive",
      "artifact": "completed tasks and fresh verification"
    },
    {
      "from": "speckit-specify",
      "to": "speckit-plan",
      "artifact": "docs/specs/<stable-feature-id>-<name>/spec.md"
    },
    {
      "from": "speckit-plan",
      "to": "architecture-modeling",
      "artifact": "docs/specs/<stable-feature-id>-<name>/plan.md"
    },
    {
      "from": "architecture-modeling",
      "to": "speckit-tasks",
      "artifact": "verified design findings"
    },
    {
      "from": "speckit-tasks",
      "to": "orchestrated-implementation",
      "artifact": "docs/specs/<stable-feature-id>-<name>/tasks.md"
    },
    {
      "from": "orchestrated-implementation",
      "to": "speckit-converge",
      "artifact": "implementation, as-built models, integration results, and review state",
      "required_gate": "architecture-modeling:as-built"
    },
    {
      "from": "speckit-converge",
      "to": "verification-before-completion",
      "artifact": "closed convergence findings",
      "completion_guard": "no actionable findings and all evidence current"
    },
    {
      "from": "openspec-propose",
      "to": "speckit-specify",
      "artifact": "docs/openspec/changes/<change-id>/escalation.md",
      "condition": "status: escalated",
      "deactivates": "openspec-propose",
      "traceability": "escalation record preserves the change path and new feature ID"
    },
    {
      "from": "openspec-apply",
      "to": "speckit-specify",
      "artifact": "docs/openspec/changes/<change-id>/escalation.md",
      "condition": "status: escalated",
      "deactivates": "openspec-apply",
      "traceability": "escalation record preserves completed task IDs, change path, and new feature ID"
    }
  ],
  "retry_transitions": [
    {
      "from": "speckit-converge",
      "to": "orchestrated-implementation",
      "condition": "actionable findings appended as new slices",
      "artifact": "tasks.md append-only convergence slices",
      "preserves": "completed work and stable task IDs"
    }
  ]
}
```

The forward phase graph remains acyclic. A convergence retry returns to the existing executor. Before convergence, that executor invokes the architecture skill in as-built mode and carries integration evidence forward. Playbook authoring/review are supporting skills under the shared [playbook policy](playbooks.md).
