from src.agent import AgentOrchestrator
from src.evidence import EvidenceLogger
from src.governance import GovernanceGateway
from src.merchants import default_merchants
from src.models import PurchaseRequest
from src.payments import PaymentMock


def build_demo() -> AgentOrchestrator:
    return AgentOrchestrator(
        merchants=default_merchants(),
        payment=PaymentMock(),
        evidence=EvidenceLogger(),
        governance=GovernanceGateway(),
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
    print("evidence=artifacts/evidence.jsonl")


if __name__ == "__main__":
    main()
