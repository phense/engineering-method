"""In-memory inventory component for the checkout fixture."""

from .models import Reservation


class InventoryCommitError(RuntimeError):
    pass


class Inventory:
    def __init__(self, events: list[str], *, fail_commit: bool = False) -> None:
        self.events = events
        self.fail_commit = fail_commit
        self.held: dict[str, Reservation] = {}
        self.committed: set[str] = set()
        self.released: set[str] = set()

    def reserve(self, order_id: str) -> Reservation:
        reservation = Reservation(order_id, f"reservation-{order_id}")
        self.held[reservation.reservation_id] = reservation
        self.events.append("inventory.reserve")
        return reservation

    def commit(self, reservation: Reservation) -> None:
        self.events.append("inventory.commit")
        if self.fail_commit:
            self.events.append("inventory.commit_failed")
            raise InventoryCommitError(reservation.reservation_id)
        self.held.pop(reservation.reservation_id)
        self.committed.add(reservation.reservation_id)

    def release(self, reservation: Reservation) -> None:
        self.held.pop(reservation.reservation_id, None)
        self.released.add(reservation.reservation_id)
        self.events.append("inventory.release")
