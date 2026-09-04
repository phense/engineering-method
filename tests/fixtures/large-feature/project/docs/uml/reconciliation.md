# As-built reconciliation

```json
{
  "verified_on": "2026-09-04",
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
