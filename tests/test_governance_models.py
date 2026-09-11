import unittest
from datetime import datetime, timezone

from src.governance import Mandate, evaluate_policies
from src.models import ProductOffer, PurchaseRequest


class GovernanceModelTests(unittest.TestCase):
    def test_valid_offer_passes_initial_policies(self):
        mandate = Mandate(
            mandate_id="mandate_test",
            max_amount=1_200_000,
            allowed_merchants=("merchant_a",),
            allowed_brands=("Sony",),
            valid_until=datetime(2026, 12, 31, tzinfo=timezone.utc),
        )
        request = PurchaseRequest("Audifonos", 1_200_000, 4, ("Sony",))
        offer = ProductOffer("merchant_a", "sony-001", "Sony Demo", "Sony", 1_000_000, 2, 2)

        results = evaluate_policies(mandate, request, offer)

        self.assertTrue(results)
        self.assertTrue(all(result.passed for result in results))

    def test_disallowed_merchant_is_detected(self):
        mandate = Mandate(
            mandate_id="mandate_test",
            max_amount=1_200_000,
            allowed_merchants=("merchant_a",),
        )
        request = PurchaseRequest("Audifonos", 1_200_000, 4)
        offer = ProductOffer("merchant_b", "demo-001", "Demo", "Sony", 900_000, 1, 2)

        results = {result.policy_id: result for result in evaluate_policies(mandate, request, offer)}

        self.assertFalse(results["ALLOWED_MERCHANT"].passed)


if __name__ == "__main__":
    unittest.main()
