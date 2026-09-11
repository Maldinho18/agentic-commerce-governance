from __future__ import annotations

from dataclasses import replace
from uuid import uuid4

from src.models import Checkout, ProductOffer, PurchaseRequest


class MerchantSimulator:
    def __init__(self, merchant_id: str, offers: list[ProductOffer]):
        self.merchant_id = merchant_id
        self._offers = offers

    def search(self, request: PurchaseRequest) -> list[ProductOffer]:
        results: list[ProductOffer] = []
        for offer in self._offers:
            if offer.stock <= 0:
                continue
            if request.product_type.lower() not in offer.name.lower():
                continue
            results.append(offer)
        return results

    def checkout(self, offer: ProductOffer) -> Checkout:
        current = next((item for item in self._offers if item.sku == offer.sku), None)
        if current is None or current.stock <= 0:
            raise ValueError("Offer is not available")
        return Checkout(
            checkout_id=f"chk_{uuid4().hex[:10]}",
            offer=current,
            total=current.price,
        )

    def create_order(self, sku: str) -> None:
        for index, offer in enumerate(self._offers):
            if offer.sku == sku:
                if offer.stock <= 0:
                    raise ValueError("Out of stock")
                self._offers[index] = replace(offer, stock=offer.stock - 1)
                return
        raise ValueError("Unknown SKU")


def default_merchants() -> dict[str, MerchantSimulator]:
    merchant_a = MerchantSimulator(
        "merchant_a",
        [
            ProductOffer("merchant_a", "A-SONY-XM6", "Audifonos Sony WH-1000XM6", "Sony", 1_100_000, 5, 2),
            ProductOffer("merchant_a", "A-BOSE-QC", "Audifonos Bose QuietComfort", "Bose", 1_160_000, 3, 2),
        ],
    )
    merchant_b = MerchantSimulator(
        "merchant_b",
        [
            ProductOffer("merchant_b", "B-SONY-XM6", "Audifonos Sony WH-1000XM6", "Sony", 1_040_000, 4, 5),
            ProductOffer("merchant_b", "B-BOSE-QC", "Audifonos Bose QuietComfort", "Bose", 1_020_000, 6, 4),
        ],
    )
    return {merchant_a.merchant_id: merchant_a, merchant_b.merchant_id: merchant_b}
