from dataclasses import dataclass
from datetime import datetime, timezone

from src.governance.mandate import Mandate
from src.models import ProductOffer, PurchaseRequest


@dataclass(frozen=True)
class PolicyResult:
    policy_id: str
    passed: bool
    reason: str


def evaluate_policies(
    mandate: Mandate,
    request: PurchaseRequest,
    offer: ProductOffer,
    now: datetime | None = None,
) -> list[PolicyResult]:
    """Evalúa las políticas base definidas para semana 6.

    V1 no usa todavía estos resultados para bloquear la compra; el objetivo actual
    es formalizar qué reglas gobernarán V2 y dejar evidencia reproducible de su
    diseño.
    """

    now = now or datetime.now(timezone.utc)
    results: list[PolicyResult] = []

    results.append(
        PolicyResult(
            "MAX_AMOUNT",
            offer.price <= mandate.max_amount,
            f"offer.price={offer.price} <= mandate.max_amount={mandate.max_amount}",
        )
    )

    merchant_allowed = not mandate.allowed_merchants or offer.merchant_id in mandate.allowed_merchants
    results.append(
        PolicyResult(
            "ALLOWED_MERCHANT",
            merchant_allowed,
            f"merchant={offer.merchant_id}",
        )
    )

    brand_allowed = not mandate.allowed_brands or offer.brand in mandate.allowed_brands
    results.append(
        PolicyResult(
            "ALLOWED_BRAND",
            brand_allowed,
            f"brand={offer.brand}",
        )
    )

    results.append(
        PolicyResult(
            "VALIDITY",
            mandate.is_active(now),
            f"valid_until={mandate.valid_until.isoformat() if mandate.valid_until else 'none'}",
        )
    )

    delivery_allowed = offer.delivery_days <= request.max_delivery_days
    results.append(
        PolicyResult(
            "DELIVERY_DEADLINE",
            delivery_allowed,
            f"delivery_days={offer.delivery_days} <= requested={request.max_delivery_days}",
        )
    )

    return results
