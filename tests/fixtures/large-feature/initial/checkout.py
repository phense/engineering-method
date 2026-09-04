"""Deliberately incomplete checkout failure path."""


class CheckoutService:
    def __init__(self, order, inventory, payment):
        self.order = order
        self.inventory = inventory
        self.payment = payment

    def checkout(self, order_id: str):
        reservation = self.inventory.reserve(order_id)
        receipt = self.payment.capture(order_id)
        try:
            self.inventory.commit(reservation)
        except RuntimeError:
            self.order.mark_failed(order_id)
            raise
        self.order.mark_complete(order_id)
        return receipt
