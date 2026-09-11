import tempfile
import unittest
from pathlib import Path

from src.agent import AgentOrchestrator
from src.evidence import EvidenceLogger
from src.governance import GovernanceGateway
from src.merchants import default_merchants
from src.models import PurchaseRequest
from src.payments import PaymentMock


class EndToEndTests(unittest.TestCase):
    def make_orchestrator(self, evidence_path: str) -> AgentOrchestrator:
        return AgentOrchestrator(
            merchants=default_merchants(),
            payment=PaymentMock(),
            evidence=EvidenceLogger(evidence_path),
            governance=GovernanceGateway(),
        )

    def test_valid_purchase_completes(self):
        with tempfile.TemporaryDirectory() as tmp:
            evidence = str(Path(tmp) / "evidence.jsonl")
            orchestrator = self.make_orchestrator(evidence)
            request = PurchaseRequest("Audifonos", 1_200_000, 4, ("Sony", "Bose"))
            order = orchestrator.run(request)

            self.assertTrue(order.order_id.startswith("ord_"))
            self.assertLessEqual(order.total, request.max_price)
            self.assertTrue(Path(evidence).exists())

    def test_no_valid_offer_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            orchestrator = self.make_orchestrator(str(Path(tmp) / "evidence.jsonl"))
            request = PurchaseRequest("Audifonos", 500_000, 2, ("Sony",))
            with self.assertRaises(ValueError):
                orchestrator.run(request)


if __name__ == "__main__":
    unittest.main()
