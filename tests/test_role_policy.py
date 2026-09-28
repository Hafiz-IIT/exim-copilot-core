import unittest

from exim_copilot_core import Case, Recommendation
from role_policy import PermissionDenied, Role, WorkflowService


class RolePolicyTests(unittest.TestCase):
    def test_trader_can_upload_but_cannot_verify(self):
        case = Case("x", {"invoice"})
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice")
        with self.assertRaises(PermissionDenied):
            service.mark_verified(Role.TRADER)

    def test_reviewer_can_verify(self):
        case = Case("x", {"invoice"})
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice")
        service.mark_verified(Role.REVIEWER)
        self.assertEqual(case.recommend(), Recommendation.ACT)

    def test_broker_can_record_discrepancy(self):
        case = Case("x", {"invoice"})
        service = WorkflowService(case)
        service.add_discrepancy(Role.BROKER, "weight mismatch")
        self.assertIn("weight mismatch", case.discrepancies)


if __name__ == "__main__":
    unittest.main()
