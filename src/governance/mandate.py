from dataclasses import dataclass
from datetime import datetime, timezone

from src.models import ProductOffer, PurchaseRequest


@dataclass(frozen=True)
class Mandate:
    """Representación mínima de autoridad delegada para el Sprint 2.

    En semana 6 el mandato se modela y documenta, pero V1 todavía no lo aplica
    como bloqueo. Esto permite cerrar el contrato de datos sin mezclar el baseline
    con los controles que se evaluarán después.
    """

    mandate_id: str
    max_amount: int
    allowed_merchants: tuple[str, ...] = ()
    allowed_brands: tuple[str, ...] = ()
    valid_until: datetime | None = None
    require_human_above: int | None = None

    def is_active(self, now: datetime | None = None) -> bool:
        if self.valid_until is None:
            return True
        now = now or datetime.now(timezone.utc)
        valid_until = self.valid_until
        if valid_until.tzinfo is None:
            valid_until = valid_until.replace(tzinfo=timezone.utc)
        return now <= valid_until

    def applies_to(self, request: PurchaseRequest, offer: ProductOffer) -> bool:
        return offer.price <= self.max_amount
