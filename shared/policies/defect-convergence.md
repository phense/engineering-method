# Defect Convergence

```json
{
  "escalation_sequence": [
    "precise_finding_to_original_implementer",
    "root_cause_and_covering_test",
    "after_two_ineffective_attempts_use_fresh_or_stronger_agent",
    "repeated_local_failure_run_interface_or_architecture_analysis"
  ],
  "fresh_perspective_after_ineffective_attempts": 2,
  "retry_progress_requires_one": ["new_evidence", "new_hypothesis", "changed_approach", "model_or_perspective_escalation"],
  "reject_identical_retry_brief": true,
  "after_each_fix": "narrowest_meaningful_covering_tests",
  "broaden_tests_only_for": ["integration_affecting_fix", "integration_boundary"],
  "terminal_conditions": ["all_actionable_findings_resolved", "external_blocker", "missing_authorization", "unsafe_irreversible_operation", "specification_contradiction"]
}
```

Every actionable review or verification finding remains open until current
evidence proves it resolved or a terminal condition is recorded. Findings are
never silently downgraded, parked, or discarded.

## Escalation sequence

1. Return the precise finding, requirement, and repository evidence to the
   original implementer.
2. Require a root-cause statement and a meaningful covering test that fails for
   the defect, or recorded evidence explaining why such a test cannot exist.
3. After two ineffective attempts, stop resending the same local framing. Use a
   fresh agent or a stronger semantic capability role and provide the prior
   evidence, hypotheses, approaches, test results, and report path.
4. When local fixes keep failing, analyze the shared interface and relevant
   architecture before another implementation attempt. Record the conclusion
   as a decision or actionable finding.

If the platform has no subagents or stronger tier, the coordinator must change
perspective or approach itself and record the unavailable escalation; it must
not claim that an agent or model changed.

## Progress gate

Before every retry, compare the new brief with the previous one. It must add at
least one of: new evidence, a new falsifiable hypothesis, a changed approach,
or a model/perspective escalation. Reject an identical retry brief. Record the
attempt number, new fact, expected discriminating result, and prior report path
in the checkpoint so recovery cannot repeat an ineffective attempt.

After every fix, run the narrowest meaningful covering tests and read their
complete result before review. Broaden tests only when the fix affects
integration or at an integration boundary; final verification remains a
separate acceptance gate.

## Terminal conditions

Continue while safe, authorized progress can be driven by evidence. Stop only
when:

- every actionable finding is resolved with current evidence;
- a recorded external blocker prevents progress;
- required authorization is missing;
- the next operation is unsafe and irreversible; or
- a specification contradiction makes another change guesswork.

For a blocker, record the precise condition, evidence and attempts, affected
work, and exact action or decision needed next. A retry budget, elapsed time,
agent eviction, or finding severity alone is not a terminal condition.
