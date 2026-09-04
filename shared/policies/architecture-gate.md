# Architecture Gate

Architecture depth is activated by current scope and risk, not by the presence
of a diagram tool.

```json
{
  "activate_for": [
    "large_cross_component_feature",
    "new_or_materially_changed_system_boundary",
    "architectural_refactor",
    "substantial_migration",
    "cross_component_concurrency_security_or_data_integrity"
  ],
  "exclude_for": ["small_fix", "localized_brownfield_change", "documentation", "mechanical_refactor"],
  "named_question_required": true,
  "omit_irrelevant_diagrams": true,
  "analysis_checks": [
    "ownership",
    "interface_mismatch",
    "dependency_cycles",
    "invalid_or_unreachable_states",
    "failure_or_rollback_gaps",
    "ordering_or_races",
    "trust_boundaries",
    "migration_consistency"
  ],
  "design_time_order": ["analyze_plan_and_repository", "create_relevant_diagrams", "write_docs/uml/findings.md", "speckit-tasks"],
  "as_built_order": ["reconcile_diagrams_against_code", "classify_every_difference", "system_architect_integration_tests"],
  "difference_dispositions": ["code_corrected", "diagram_corrected_with_rationale", "unresolved_defect"]
}
```

## Activation decision

Record the concrete scope or risk evidence that matches one activation
category. If none matches—or the work is a small fix, localized Brownfield
change, documentation, or mechanical refactor—do not create UML artifacts.

## Relevant diagrams only

Every diagram begins with one named design or verification question. Choose
the smallest notation that answers it and omit every diagram whose answer
would not affect a decision, finding, integration test, or verification.
Diagram count is never a completion criterion.

## Evidence and order

Design-time models are checked against the approved plan and repository.
Write every actionable result to `docs/uml/findings.md` with a stable finding
ID before `speckit-tasks`; task generation must carry each open finding as
normal work.

After implementation, reconcile the relevant diagrams against actual code
before the system architect derives integration tests. Classify every
difference as code corrected, diagram corrected with rationale, or unresolved
defect. An unresolved defect remains actionable through convergence.
