# Tasks: Checkout consistency

```json
{
  "work_id": "F-001",
  "architecture_findings": ["AF-001", "AF-002"],
  "task_order": ["T001", "T002", "T003", "T004"],
  "tasks": [
    {"id": "T001", "finding_id": "AF-001", "kind": "architecture_finding", "outcome": "reserve returns Reservation across the order/inventory boundary"},
    {"id": "T002", "finding_id": "AF-002", "kind": "architecture_finding", "outcome": "commit failure releases inventory and reverses payment"},
    {"id": "T003", "finding_id": null, "kind": "implementation", "outcome": "checkout success completes all components"},
    {"id": "T004", "finding_id": null, "kind": "integration", "outcome": "as-built diagrams and derived integration tests pass"}
  ]
}
```

## Architecture findings

- [x] T001 [AF-001] Align `InventoryPort.reserve` and `Inventory.reserve` on `Reservation`; verify the real boundary.
- [x] T002 [AF-002] On commit failure release the reservation, reverse captured payment, and mark the order failed; verify ordered side effects.

## Implementation slices

### Slice S1: Stable inventory reservation contract

- [x] T001 [AF-001] Implement and test the shared return contract.

### Slice S2: Checkout success and recovery

- [x] T002 [AF-002] Implement the compensation path after S1 stabilizes the interface.
- [x] T003 Implement the successful checkout flow.
- [x] T004 Reconcile as-built models and run diagram-derived integration tests.
