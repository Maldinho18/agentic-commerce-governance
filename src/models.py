from dataclasses import dataclass, asdict
from typing import Optional


@dataclass(frozen=True)
class PurchaseRequest:
    product_type: str
    max_price: int
    max_delivery_days: int
    preferred_brands: tuple[str, ...] = ()


@dataclass(frozen=True)
class ProductOffer:
    merchant_id: str
    sku: str
    name: str
    brand: str
    price: int
    stock: int
    delivery_days: int


@dataclass(frozen=True)
class Checkout:
    checkout_id: str
    offer: ProductOffer
    total: int


@dataclass(frozen=True)
class PaymentResult:
    payment_id: str
    approved: bool
    reason: str = ""


@dataclass(frozen=True)
class Order:
    order_id: str
    checkout_id: str
    merchant_id: str
    sku: str
    total: int
    payment_id: str


def to_dict(value):
    return asdict(value)
