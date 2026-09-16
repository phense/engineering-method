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
    "speckit-converge",
    "documentation-planning",
    "documentation-authoring",
    "documentation-review"
  ],
  "executors": {
    "bugfix": "test-driven-development",
    "openspec": "openspec-apply",
    "speckit": "orchestrated-implementation",
    "documentation": "documentation-authoring"
  },
  "edges": [
    {"from": "systematic-debugging", "to": "test-driven-development", "artifact": "reproduction and root-cause evidence"},
    {"from": "systematic-debugging", "to": "openspec-propose", "artifact": "docs/openspec/changes/<change-id>/proposal.md", "condition": "evidence establishes a bounded intentional contract change", "deactivates": "systematic-debugging", "traceability": "proposal links the reproduction and root-cause evidence"},
    {"from": "systematic-debugging", "to": "speckit-specify", "artifact": "docs/specs/<stable-feature-id>-<name>/spec.md", "condition": "evidence establishes an architecture change or large-feature scope", "deactivates": "systematic-debugging", "traceability": "feature spec links the reproduction and root-cause evidence"},
    {"from": "test-driven-development", "to": "verification-before-completion", "artifact": "verified red-green evidence"},
    {"from": "openspec-propose", "to": "openspec-apply", "artifact": "docs/openspec/changes/<change-id>/tasks.md"},
    {"from": "openspec-apply", "to": "openspec-archive", "artifact": "completed tasks and fresh verification"},
    {"from": "speckit-specify", "to": "speckit-plan", "artifact": "docs/specs/<stable-feature-id>-<name>/spec.md"},
    {"from": "speckit-plan", "to": "architecture-modeling", "artifact": "docs/specs/<stable-feature-id>-<name>/plan.md"},
    {"from": "architecture-modeling", "to": "speckit-tasks", "artifact": "verified design findings"},
    {"from": "speckit-tasks", "to": "orchestrated-implementation", "artifact": "docs/specs/<stable-feature-id>-<name>/tasks.md"},
    {"from": "orchestrated-implementation", "to": "speckit-converge", "artifact": "implementation, as-built models, integration results, and review state", "required_gate": "architecture-modeling:as-built"},
    {"from": "speckit-converge", "to": "verification-before-completion", "artifact": "closed convergence findings", "completion_guard": "no actionable findings and all evidence current"},
    {"from": "openspec-propose", "to": "speckit-specify", "artifact": "docs/openspec/changes/<change-id>/escalation.md", "condition": "status: escalated", "deactivates": "openspec-propose", "traceability": "escalation record preserves the change path and new feature ID"},
    {"from": "openspec-apply", "to": "speckit-specify", "artifact": "docs/openspec/changes/<change-id>/escalation.md", "condition": "status: escalated", "deactivates": "openspec-apply", "traceability": "escalation record preserves completed task IDs, change path, and new feature ID"},
    {"from": "documentation-planning", "to": "documentation-authoring", "artifact": "docs/writing/<doc-id>/plan.md"},
    {"from": "documentation-authoring", "to": "documentation-review", "artifact": "drafted chunk files with frontmatter, glossary and asset manifest state"},
    {"from": "documentation-review", "to": "verification-before-completion", "artifact": "docs/writing/<doc-id>/review.md", "completion_guard": "no open Critical or Important findings at the reviewed revision"}
  ],
  "retry_transitions": [
    {"from": "speckit-converge", "to": "orchestrated-implementation", "condition": "actionable findings appended as new slices", "artifact": "tasks.md append-only convergence slices", "preserves": "completed work and stable task IDs"},
    {"from": "documentation-review", "to": "documentation-authoring", "condition": "actionable findings returned for affected chunks", "artifact": "docs/writing/<doc-id>/review.md findings", "preserves": "accepted chunks and stable chunk IDs"}
  ]
}
```

Reclassification and escalation edges are exceptional. Deactivate the prior
lifecycle before the destination becomes active and preserve the source
evidence, stable IDs, and artifact path named by the edge. For OpenSpec,
preserve the change and write the formal escalation record before Spec Kit
starts.

The forward phase graph remains acyclic. A convergence retry, or a documentation
review returning findings, is an explicit return to the existing executor,
never a new controller or a completion handoff. Before convergence, that executor invokes the architecture skill in
as-built mode and carries its reconciliation and integration evidence forward.

## Documentation lifecycle

Reader-facing documentation follows the [writing-depth policy](writing-depth.md).
A documentation set runs `documentation-planning` → `documentation-authoring`
→ `documentation-review` → `verification-before-completion`; review findings
return to the same authoring executor. A standalone document enters
`documentation-authoring` directly and closes with a recorded self-review. The
documentation lifecycle never shares a work ID with an engineering lifecycle;
software behavior stays with Spec Kit, OpenSpec or debugging.
