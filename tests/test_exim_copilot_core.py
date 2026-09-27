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


if __name__ == "__main__":
    unittest.main()
