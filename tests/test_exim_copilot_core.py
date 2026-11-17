import unittest

from exim_copilot_core import Case, Recommendation


class CopilotCoreTests(unittest.TestCase):
    def test_missing_document_asks(self):
        case = Case("x", {"invoice", "packing_list"})
        case.add_document("invoice")
        self.assertEqual(case.recommend(), Recommendation.ASK)

    def test_complete_but_unverified_verifies(self):
        case = Case("x", {"invoice"})
        case.add_document("invoice")
        self.assertEqual(case.recommend(), Recommendation.VERIFY)

    def test_verified_clean_case_acts(self):
        case = Case("x", {"invoice"})
        case.add_document("invoice")
        case.mark_verified()
        self.assertEqual(case.recommend(), Recommendation.ACT)

    def test_high_risk_discrepancy_escalates(self):
        case = Case("x", {"invoice"}, high_risk=True)
        case.add_document("invoice")
        case.add_discrepancy("weight mismatch")
        self.assertEqual(case.recommend(), Recommendation.ESCALATE)

    def test_new_document_invalidates_previous_verification(self):
        case = Case("x", {"invoice", "packing_list"})
        case.add_document("invoice")
        case.add_document("packing_list")
        case.mark_verified()
        self.assertEqual(case.recommend(), Recommendation.ACT)

        case.add_document("certificate_of_origin")
        self.assertFalse(case.verification_complete)
        self.assertEqual(case.recommend(), Recommendation.VERIFY)
        self.assertIn("verification:invalidated:document_added", case.events)

    def test_new_discrepancy_invalidates_previous_verification(self):
        case = Case("x", {"invoice"})
        case.add_document("invoice")
        case.mark_verified()
        case.add_discrepancy("weight mismatch")
        self.assertFalse(case.verification_complete)
        self.assertEqual(case.recommend(), Recommendation.VERIFY)
        self.assertIn("verification:invalidated:discrepancy_added", case.events)

    def test_readding_existing_document_does_not_invalidate_verification(self):
        case = Case("x", {"invoice"})
        case.add_document("invoice")
        case.mark_verified()
        case.add_document("invoice")
        self.assertTrue(case.verification_complete)
        self.assertEqual(case.recommend(), Recommendation.ACT)


if __name__ == "__main__":
    unittest.main()
