"""Deliberately mismatched inventory snapshot used by architecture analysis."""


class Inventory:
    def reserve(self, order_id: str) -> bool:
        return bool(order_id)

    def commit(self, reservation: bool) -> None:
        raise RuntimeError("inventory commit failed")

    def release(self, reservation: bool) -> None:
        pass
