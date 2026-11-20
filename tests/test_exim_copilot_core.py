import unittest

from exim_copilot_core import Case, Recommendation
from role_policy import PermissionDenied, Role, WorkflowService


class CopilotCoreTests(unittest.TestCase):
    def test_missing_document_asks(self):
        case = Case("x", {"invoice", "packing_list"})
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice", actor_id="trader-1")
        self.assertEqual(case.recommend(), Recommendation.ASK)

    def test_complete_but_unverified_verifies(self):
        case = Case("x", {"invoice"})
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice", actor_id="trader-1")
        self.assertEqual(case.recommend(), Recommendation.VERIFY)

    def test_verifier_cannot_be_document_uploader(self):
        case = Case("x", {"invoice"})
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice", actor_id="same-person")
        with self.assertRaises(PermissionError):
            service.mark_verified(Role.REVIEWER, actor_id="same-person")

    def test_high_risk_requires_two_distinct_reviewers(self):
        case = Case("x", {"invoice"}, high_risk=True)
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice", actor_id="trader")
        service.mark_verified(Role.REVIEWER, actor_id="reviewer-1")
        self.assertFalse(case.verification_complete)
        self.assertEqual(case.recommend(), Recommendation.VERIFY)
        service.mark_verified(Role.REVIEWER, actor_id="reviewer-2")
        self.assertTrue(case.verification_complete)
        self.assertEqual(case.recommend(), Recommendation.ACT)

    def test_discrepancy_must_be_resolved_before_verification(self):
        case = Case("x", {"invoice"})
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice", actor_id="trader")
        service.add_discrepancy(Role.BROKER, "weight mismatch", actor_id="broker")
        with self.assertRaises(RuntimeError):
            service.mark_verified(Role.REVIEWER, actor_id="reviewer")
        service.resolve_discrepancy(Role.REVIEWER, "weight mismatch", actor_id="reviewer")
        service.mark_verified(Role.REVIEWER, actor_id="reviewer")
        self.assertEqual(case.recommend(), Recommendation.ACT)

    def test_high_risk_discrepancy_escalates(self):
        case = Case("x", {"invoice"}, high_risk=True)
        service = WorkflowService(case)
        service.add_document(Role.TRADER, "invoice", actor_id="trader")
        service.add_discrepancy(Role.BROKER, "weight mismatch", actor_id="broker")
        self.assertEqual(case.recommend(), Recommendation.ESCALATE)


if __name__ == "__main__":
    unittest.main()
