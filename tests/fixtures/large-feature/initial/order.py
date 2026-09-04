"""Order component consuming the intended inventory contract."""

from .contracts import InventoryPort, Reservation


class OrderService:
    def __init__(self, inventory: InventoryPort) -> None:
        self.inventory = inventory
        self.states: dict[str, str] = {}

    def reserve(self, order_id: str) -> Reservation:
        self.states[order_id] = "Reserved"
        return self.inventory.reserve(order_id)

    def mark_complete(self, order_id: str) -> None:
        self.states[order_id] = "Complete"

    def mark_failed(self, order_id: str) -> None:
        self.states[order_id] = "Failed"
