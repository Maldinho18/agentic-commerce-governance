from datetime import datetime, timezone

from src.agent import AgentOrchestrator
from src.evidence import EvidenceLogger
from src.governance import GovernanceGateway, Mandate
from src.merchants import default_merchants
from src.models import PurchaseRequest
from src.payments import PaymentMock


def build_demo() -> AgentOrchestrator:
    mandate = Mandate(
        mandate_id="mandate_demo_001",
        max_amount=1_200_000,
        allowed_merchants=("merchant_a", "merchant_b"),
        allowed_brands=("Sony", "Bose"),
        valid_until=datetime(2026, 12, 31, tzinfo=timezone.utc),
        require_human_above=1_100_000,
    )

    return AgentOrchestrator(
        merchants=default_merchants(),
        payment=PaymentMock(),
        evidence=EvidenceLogger(),
        governance=GovernanceGateway(mandate=mandate),
    )


def main() -> None:
    request = PurchaseRequest(
        product_type="Audifonos",
        max_price=1_200_000,
        max_delivery_days=4,
        preferred_brands=("Sony", "Bose"),
    )
    order = build_demo().run(request)
    print("Compra simulada completada")
    print(f"order_id={order.order_id}")
    print(f"merchant={order.merchant_id}")
    print(f"sku={order.sku}")
    print(f"total={order.total}")
    print("governance=bypass_v1 (mandato y políticas inspeccionados, no aplicados)")
    print("evidence=artifacts/evidence.jsonl")


if __name__ == "__main__":
    main()
