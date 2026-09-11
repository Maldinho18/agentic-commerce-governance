from __future__ import annotations

from uuid import uuid4

from src.evidence import EvidenceLogger
from src.governance import GovernanceGateway
from src.merchants import MerchantSimulator
from src.models import Order, ProductOffer, PurchaseRequest, to_dict
from src.payments import PaymentMock


class AgentOrchestrator:
    def __init__(
        self,
        merchants: dict[str, MerchantSimulator],
        payment: PaymentMock,
        evidence: EvidenceLogger,
        governance: GovernanceGateway,
    ):
        self.merchants = merchants
        self.payment = payment
        self.evidence = evidence
        self.governance = governance

    def discover(self, request: PurchaseRequest) -> list[ProductOffer]:
        offers: list[ProductOffer] = []
        for merchant in self.merchants.values():
            offers.extend(merchant.search(request))
        self.evidence.record("discovery_completed", {"request": to_dict(request), "offers": [to_dict(o) for o in offers]})
        return offers

    def select_offer(self, request: PurchaseRequest, offers: list[ProductOffer]) -> ProductOffer:
        candidates = [
            offer for offer in offers
            if offer.price <= request.max_price
            and offer.delivery_days <= request.max_delivery_days
            and (not request.preferred_brands or offer.brand in request.preferred_brands)
        ]
        if not candidates:
            raise ValueError("No offer satisfies the purchase constraints")
        selected = min(candidates, key=lambda offer: (offer.price, offer.delivery_days))
        self.evidence.record("offer_selected", {"selected": to_dict(selected), "strategy": "lowest_price_then_delivery"})
        return selected

    def run(self, request: PurchaseRequest) -> Order:
        offers = self.discover(request)
        selected = self.select_offer(request, offers)

        allowed, reason = self.governance.authorize(request, selected)
        self.evidence.record("governance_evaluated", {"mode": self.governance.mode, "allowed": allowed, "reason": reason})
        if not allowed:
            raise PermissionError(reason)

        merchant = self.merchants[selected.merchant_id]
        checkout = merchant.checkout(selected)
        self.evidence.record("checkout_created", to_dict(checkout))

        payment_result = self.payment.pay(checkout)
        self.evidence.record("payment_processed", to_dict(payment_result))
        if not payment_result.approved:
            raise RuntimeError(payment_result.reason)

        merchant.create_order(selected.sku)
        order = Order(
            order_id=f"ord_{uuid4().hex[:10]}",
            checkout_id=checkout.checkout_id,
            merchant_id=selected.merchant_id,
            sku=selected.sku,
            total=checkout.total,
            payment_id=payment_result.payment_id,
        )
        self.evidence.record("order_created", to_dict(order))
        return order
