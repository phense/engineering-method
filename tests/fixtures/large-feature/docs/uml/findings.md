# Design-time architecture findings

```json
{
  "created_phase": "design_time_before_tasks",
  "findings": [
    {
      "id": "AF-001",
      "category": "interface_mismatch",
      "requirement_ids": ["CHECKOUT-001"],
      "evidence": ["initial/contracts.py", "initial/inventory.py", "docs/uml/design-component.mmd"],
      "required_task": "T001",
      "initial_status": "open",
      "final_status": "resolved"
    },
    {
      "id": "AF-002",
      "category": "failure_or_rollback_gap",
      "requirement_ids": ["CHECKOUT-002"],
      "evidence": ["initial/checkout.py", "docs/uml/design-recovery-sequence.mmd", "docs/uml/design-state.mmd"],
      "required_task": "T002",
      "initial_status": "open",
      "final_status": "resolved"
    }
  ]
}
```

## AF-001 — reserve return contract mismatch

Order requires a `Reservation` carrying the stable reservation identity, while
inventory returns `bool`. T001 must align the implementation and contract and
add an integration assertion on the returned reservation.

## AF-002 — missing commit-failure compensation

After payment capture, an inventory commit failure transitions directly to
Failed without inventory release or payment reversal. T002 must implement both
compensations, model their order, and add a recovery integration test.
