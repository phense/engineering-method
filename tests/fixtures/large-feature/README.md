# Checkout architecture fixture

This dependency-free fixture preserves a deliberately broken design snapshot
and a corrected as-built checkout project.

The initial order contract requires `reserve(order_id) -> Reservation`, while
the initial inventory implementation returns `bool`. Its payment-success,
inventory-commit-failure path also omits both inventory release and payment
reversal. Design-time component, sequence, and state evidence produces AF-001
and AF-002 before Spec Kit tasks are generated.

The project snapshot resolves both findings, reconciles four as-built views,
and contains one success plus one rollback integration test. Evidence files
show the five conditions required before convergence; the enclosing test suite
reruns the integration command rather than trusting the recorded result.
