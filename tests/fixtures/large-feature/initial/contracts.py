"""Intended checkout interfaces before implementation correction."""

from dataclasses import dataclass
from typing import Protocol


@dataclass(frozen=True)
class Reservation:
    order_id: str
    reservation_id: str


class InventoryPort(Protocol):
    def reserve(self, order_id: str) -> Reservation: ...

    def commit(self, reservation: Reservation) -> None: ...

    def release(self, reservation: Reservation) -> None: ...
