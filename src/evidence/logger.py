from __future__ import annotations

import json
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


class EvidenceLogger:
    """Registra evidencia estructurada y atribución técnica del flujo.

    Los campos de atribución permiten reconstruir no solo qué ocurrió, sino qué
    actor/componente produjo cada acción y, cuando aplique, qué mandato o política
    estuvo asociado a la decisión.
    """

    def __init__(self, path: str = "artifacts/evidence.jsonl"):
        self.path = Path(path)

    def record(
        self,
        event_type: str,
        payload: dict[str, Any],
        *,
        transaction_id: str | None = None,
        actor: str | None = None,
        component: str | None = None,
        action: str | None = None,
        decision_id: str | None = None,
        mandate_id: str | None = None,
        policy_id: str | None = None,
        result: str | None = None,
    ) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        event = {
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "event_type": event_type,
            "transaction_id": transaction_id,
            "actor": actor,
            "component": component,
            "action": action,
            "decision_id": decision_id,
            "mandate_id": mandate_id,
            "policy_id": policy_id,
            "result": result,
            "payload": payload,
        }
        with self.path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(event, ensure_ascii=False) + "\n")
