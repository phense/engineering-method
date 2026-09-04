"""Checkout orchestration with ordered compensation."""

from .inventory import InventoryCommitError
from .models import CheckoutResult
from .order import OrderService
from .payment import Payment


class CheckoutService:
    def __init__(self, order: OrderService, payment: Payment) -> None:
        self.order = order
        self.inventory = order.inventory
        self.payment = payment

    def checkout(self, order_id: str) -> CheckoutResult:
        reservation = self.order.reserve(order_id)
        receipt = self.payment.capture(order_id)
        self.order.mark_paid(order_id)
        try:
            self.inventory.commit(reservation)
        except InventoryCommitError:
            self.order.mark_compensating(order_id)
            self.inventory.release(reservation)
            self.payment.reverse(receipt)
            self.order.mark_failed(order_id)
            raise
        self.order.mark_complete(order_id)
        return CheckoutResult(order_id, reservation.reservation_id, receipt.payment_id)
