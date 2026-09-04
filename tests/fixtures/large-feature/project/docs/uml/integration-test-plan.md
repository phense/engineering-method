# Checkout integration test plan

- Reconciled component diagram: `docs/uml/component.mmd`
- Reconciled success sequence: `docs/uml/success-sequence.mmd`
- Reconciled recovery sequence: `docs/uml/recovery-sequence.mmd`
- Reconciled state diagram: `docs/uml/state.mmd`
- Reconciliation evidence: `docs/uml/reconciliation.md`

## IT-SUCCESS-001

`integration_tests.test_checkout.CheckoutIntegrationTests.test_checkout_success_matches_success_sequence`
exercises Inventory, OrderService, Payment, and CheckoutService and asserts the
literal cross-component event order plus committed state.

## IT-RECOVERY-001

`integration_tests.test_checkout.CheckoutIntegrationTests.test_commit_failure_releases_inventory_and_reverses_payment`
injects inventory commit failure and asserts release, reversal, failed order
state, the explicit Compensating transition, absence of held
inventory/captured payment, and literal compensation order.

Command: `python3 -m unittest discover -s integration_tests -v`
