"""System-architect tests derived from reconciled checkout diagrams."""

import unittest

from checkout import CheckoutService, Inventory, InventoryCommitError, OrderService, Payment


class CheckoutIntegrationTests(unittest.TestCase):
    def test_checkout_success_matches_success_sequence(self) -> None:
        events: list[str] = []
        inventory = Inventory(events)
        order = OrderService(inventory, events)
        payment = Payment(events)

        result = CheckoutService(order, payment).checkout("order-1")

        self.assertEqual("reservation-order-1", result.reservation_id)
        self.assertEqual("payment-order-1", result.payment_id)
        self.assertEqual("Complete", order.states["order-1"])
        self.assertEqual({"reservation-order-1"}, inventory.committed)
        self.assertEqual({"payment-order-1"}, set(payment.captured))
        self.assertEqual(set(), payment.reversed)
        self.assertEqual(
            [
                "inventory.reserve",
                "payment.capture",
                "order.paid",
                "inventory.commit",
                "order.complete",
            ],
            events,
        )

    def test_commit_failure_releases_inventory_and_reverses_payment(self) -> None:
        events: list[str] = []
        inventory = Inventory(events, fail_commit=True)
        order = OrderService(inventory, events)
        payment = Payment(events)

        with self.assertRaises(InventoryCommitError):
            CheckoutService(order, payment).checkout("order-2")

        self.assertEqual("Failed", order.states["order-2"])
        self.assertEqual({}, inventory.held)
        self.assertEqual({"reservation-order-2"}, inventory.released)
        self.assertEqual({}, payment.captured)
        self.assertEqual({"payment-order-2"}, payment.reversed)
        self.assertEqual(
            [
                "inventory.reserve",
                "payment.capture",
                "order.paid",
                "inventory.commit",
                "inventory.commit_failed",
                "order.compensating",
                "inventory.release",
                "payment.reverse",
                "order.failed",
            ],
            events,
        )


if __name__ == "__main__":
    unittest.main()
