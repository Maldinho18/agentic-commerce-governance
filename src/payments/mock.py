from uuid import uuid4

from src.models import Checkout, PaymentResult


class PaymentMock:
    """Deterministic sandbox payment: approves positive totals only."""

    def pay(self, checkout: Checkout) -> PaymentResult:
        if checkout.total <= 0:
            return PaymentResult(f"pay_{uuid4().hex[:10]}", False, "invalid_total")
        return PaymentResult(f"pay_{uuid4().hex[:10]}", True, "approved")
