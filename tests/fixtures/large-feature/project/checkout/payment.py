"""In-memory payment component for the checkout fixture."""

from .models import PaymentReceipt


class Payment:
    def __init__(self, events: list[str]) -> None:
        self.events = events
        self.captured: dict[str, PaymentReceipt] = {}
        self.reversed: set[str] = set()

    def capture(self, order_id: str) -> PaymentReceipt:
        receipt = PaymentReceipt(order_id, f"payment-{order_id}")
        self.captured[receipt.payment_id] = receipt
        self.events.append("payment.capture")
        return receipt

    def reverse(self, receipt: PaymentReceipt) -> None:
        self.captured.pop(receipt.payment_id, None)
        self.reversed.add(receipt.payment_id)
        self.events.append("payment.reverse")
