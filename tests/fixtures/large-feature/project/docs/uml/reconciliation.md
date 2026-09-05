# As-built reconciliation

```json
{
  "verified_on": "2026-09-05",
  "differences": [
    {"finding_id": "AF-001", "disposition": "code_corrected", "evidence": ["checkout/ports.py", "checkout/inventory.py", "component.mmd"]},
    {"finding_id": "AF-002", "disposition": "code_corrected", "evidence": ["checkout/service.py", "recovery-sequence.mmd", "state.mmd"]}
  ],
  "unresolved_defects": []
}
```

The order-required and inventory-provided reserve contracts both return
`Reservation`. The commit-failure path now releases inventory, reverses the
captured payment, marks the order failed, and re-raises the original failure.

Diagram corrections with rationale: the as-built state view starts at Reserved
because OrderService never stores a Pending state. The component view includes
CheckoutService's direct commit/release dependency on Inventory, which the
implementation accesses through OrderService.inventory. Both corrections are
checked against live integration paths by the fixture acceptance oracle.
