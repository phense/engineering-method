"""Cross-component checkout contracts."""

from typing import Protocol

from .models import PaymentReceipt, Reservation


class InventoryPort(Protocol):
    def reserve(self, order_id: str) -> Reservation: ...

    def commit(self, reservation: Reservation) -> None: ...

    def release(self, reservation: Reservation) -> None: ...


class PaymentPort(Protocol):
    def capture(self, order_id: str) -> PaymentReceipt: ...

    def reverse(self, receipt: PaymentReceipt) -> None: ...
