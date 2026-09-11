from __future__ import annotations

from src.governance.mandate import Mandate
from src.governance.policies import PolicyResult, evaluate_policies
from src.models import ProductOffer, PurchaseRequest


class GovernanceGateway:
    """Punto de control entre decisión y ejecución.

    En V1 el modo permanece en `bypass`: las políticas se pueden evaluar y registrar
    como evidencia de diseño, pero todavía no bloquean la compra. En Sprint 2 este
    mismo gateway pasará a enforcement para comparar V1 vs V2 sobre el mismo flujo.
    """

    mode = "bypass"

    def __init__(self, mandate: Mandate | None = None):
        self.mandate = mandate

    def inspect(self, request: PurchaseRequest, offer: ProductOffer) -> list[PolicyResult]:
        if self.mandate is None:
            return []
        return evaluate_policies(self.mandate, request, offer)

    def authorize(self, request: PurchaseRequest, offer: ProductOffer) -> tuple[bool, str]:
        # Sprint 1 baseline: deliberadamente no se hace enforcement.
        return True, "bypass_v1"
