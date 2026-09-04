"""Values exchanged by checkout components."""

from dataclasses import dataclass


@dataclass(frozen=True)
class Reservation:
    order_id: str
    reservation_id: str


@dataclass(frozen=True)
class PaymentReceipt:
    order_id: str
    payment_id: str


@dataclass(frozen=True)
class CheckoutResult:
    order_id: str
    reservation_id: str
    payment_id: str
