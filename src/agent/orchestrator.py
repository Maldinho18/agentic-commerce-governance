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

    def discover(self, request: PurchaseRequest, transaction_id: str) -> list[ProductOffer]:
        offers: list[ProductOffer] = []
        for merchant in self.merchants.values():
            offers.extend(merchant.search(request))
        self.evidence.record(
            "discovery_completed",
            {"request": to_dict(request), "offers": [to_dict(o) for o in offers]},
            transaction_id=transaction_id,
            actor="agent",
            component="AgentOrchestrator",
            action="discover_offers",
            result=f"{len(offers)}_offers",
        )
        return offers

    def select_offer(
        self,
        request: PurchaseRequest,
        offers: list[ProductOffer],
        transaction_id: str,
    ) -> tuple[ProductOffer, str]:
        candidates = [
            offer for offer in offers
            if offer.price <= request.max_price
            and offer.delivery_days <= request.max_delivery_days
            and (not request.preferred_brands or offer.brand in request.preferred_brands)
        ]
        if not candidates:
            raise ValueError("No offer satisfies the purchase constraints")
        selected = min(candidates, key=lambda offer: (offer.price, offer.delivery_days))
        decision_id = f"dec_{uuid4().hex[:10]}"
        self.evidence.record(
            "offer_selected",
            {"selected": to_dict(selected), "strategy": "lowest_price_then_delivery"},
            transaction_id=transaction_id,
            actor="agent",
            component="AgentOrchestrator",
            action="select_offer",
            decision_id=decision_id,
            result=f"{selected.merchant_id}:{selected.sku}",
        )
        return selected, decision_id

    def run(self, request: PurchaseRequest) -> Order:
        transaction_id = f"tx_{uuid4().hex[:10]}"
        offers = self.discover(request, transaction_id)
        selected, decision_id = self.select_offer(request, offers, transaction_id)

        for policy_result in self.governance.inspect(request, selected):
            self.evidence.record(
                "policy_inspected",
                {"passed": policy_result.passed, "reason": policy_result.reason},
                transaction_id=transaction_id,
                actor="governance",
                component="GovernanceGateway",
                action="inspect_policy",
                decision_id=decision_id,
                mandate_id=(self.governance.mandate.mandate_id if self.governance.mandate else None),
                policy_id=policy_result.policy_id,
                result="PASS" if policy_result.passed else "FAIL",
            )

        allowed, reason = self.governance.authorize(request, selected)
        self.evidence.record(
            "governance_evaluated",
            {"mode": self.governance.mode, "allowed": allowed, "reason": reason},
            transaction_id=transaction_id,
            actor="governance",
            component="GovernanceGateway",
            action="authorize",
            decision_id=decision_id,
            mandate_id=(self.governance.mandate.mandate_id if self.governance.mandate else None),
            result="ALLOW" if allowed else "BLOCK",
        )
        if not allowed:
            raise PermissionError(reason)

        merchant = self.merchants[selected.merchant_id]
        checkout = merchant.checkout(selected)
        self.evidence.record(
            "checkout_created",
            to_dict(checkout),
            transaction_id=transaction_id,
            actor="merchant",
            component=f"MerchantSimulator:{selected.merchant_id}",
            action="create_checkout",
            decision_id=decision_id,
            result=checkout.checkout_id,
        )

        payment_result = self.payment.pay(checkout)
        self.evidence.record(
            "payment_processed",
            to_dict(payment_result),
            transaction_id=transaction_id,
            actor="payment_provider",
            component="PaymentMock",
            action="process_payment",
            decision_id=decision_id,
            result="APPROVED" if payment_result.approved else "DECLINED",
        )
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
        self.evidence.record(
            "order_created",
            to_dict(order),
            transaction_id=transaction_id,
            actor="merchant",
            component=f"MerchantSimulator:{selected.merchant_id}",
            action="create_order",
            decision_id=decision_id,
            result=order.order_id,
        )
        return order
