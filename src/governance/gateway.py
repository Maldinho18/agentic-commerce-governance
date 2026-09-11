from src.models import ProductOffer, PurchaseRequest


class GovernanceGateway:
    """V1 extension point. Sprint 2 will replace bypass with mandate/policy checks."""

    mode = "bypass"

    def authorize(self, request: PurchaseRequest, offer: ProductOffer) -> tuple[bool, str]:
        return True, "bypass_v1"
