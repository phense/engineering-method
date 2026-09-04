"""Order component consuming the inventory contract."""

from .models import Reservation
from .ports import InventoryPort


class OrderService:
    def __init__(self, inventory: InventoryPort, events: list[str]) -> None:
        self.inventory = inventory
        self.events = events
        self.states: dict[str, str] = {}

    def reserve(self, order_id: str) -> Reservation:
        self.states[order_id] = "Reserved"
        return self.inventory.reserve(order_id)

    def mark_paid(self, order_id: str) -> None:
        self.states[order_id] = "Paid"
        self.events.append("order.paid")

    def mark_complete(self, order_id: str) -> None:
        self.states[order_id] = "Complete"
        self.events.append("order.complete")

    def mark_compensating(self, order_id: str) -> None:
        self.states[order_id] = "Compensating"
        self.events.append("order.compensating")

    def mark_failed(self, order_id: str) -> None:
        self.states[order_id] = "Failed"
        self.events.append("order.failed")
