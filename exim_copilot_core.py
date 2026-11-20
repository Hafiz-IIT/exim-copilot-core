from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum


class Recommendation(str, Enum):
    ACT = "ACT"
    ASK = "ASK"
    VERIFY = "VERIFY"
    ESCALATE = "ESCALATE"


@dataclass
class Case:
    case_id: str
    required_documents: set[str]
    received_documents: set[str] = field(default_factory=set)
    discrepancies: list[str] = field(default_factory=list)
    verification_complete: bool = False
    high_risk: bool = False
    events: list[str] = field(default_factory=list)
    uploaded_by: set[str] = field(default_factory=set)
    verification_actors: set[str] = field(default_factory=set)

    @staticmethod
    def _actor(actor_id: str) -> None:
        if not isinstance(actor_id, str) or not actor_id.strip():
            raise ValueError("actor_id must be a non-empty string")

    def _add_document(self, kind: str, actor_id: str) -> None:
        self._actor(actor_id)
        if not isinstance(kind, str) or not kind.strip():
            raise ValueError("document kind must be non-empty")
        self.received_documents.add(kind)
        self.uploaded_by.add(actor_id)
        self.verification_complete = False
        self.verification_actors.clear()
        self.events.append(f"actor:{actor_id}:document:{kind}")

    def _add_discrepancy(self, detail: str, actor_id: str) -> None:
        self._actor(actor_id)
        if not isinstance(detail, str) or not detail.strip():
            raise ValueError("discrepancy detail must be non-empty")
        self.discrepancies.append(detail)
        self.verification_complete = False
        self.verification_actors.clear()
        self.events.append(f"actor:{actor_id}:discrepancy:{detail}")

    def _resolve_discrepancy(self, detail: str, actor_id: str) -> None:
        self._actor(actor_id)
        if detail not in self.discrepancies:
            raise KeyError(detail)
        self.discrepancies.remove(detail)
        self.verification_complete = False
        self.verification_actors.clear()
        self.events.append(f"actor:{actor_id}:discrepancy-resolved:{detail}")

    def _record_verification(self, actor_id: str) -> None:
        self._actor(actor_id)
        if actor_id in self.uploaded_by:
            raise PermissionError("a document uploader cannot verify their own case")
        if self.missing_documents:
            raise RuntimeError("cannot verify while required documents are missing")
        if self.discrepancies:
            raise RuntimeError("cannot verify while discrepancies remain unresolved")
        self.verification_actors.add(actor_id)
        required_reviewers = 2 if self.high_risk else 1
        self.verification_complete = len(self.verification_actors) >= required_reviewers
        self.events.append(f"actor:{actor_id}:verification-review")
        if self.verification_complete:
            self.events.append("verification:complete")

    @property
    def missing_documents(self) -> set[str]:
        return self.required_documents - self.received_documents

    def recommend(self) -> Recommendation:
        if self.high_risk and self.discrepancies:
            return Recommendation.ESCALATE
        if self.missing_documents:
            return Recommendation.ASK
        if self.discrepancies or not self.verification_complete:
            return Recommendation.VERIFY
        return Recommendation.ACT

    def evidence_packet(self) -> dict:
        return {
            "case_id": self.case_id,
            "received_documents": sorted(self.received_documents),
            "missing_documents": sorted(self.missing_documents),
            "discrepancies": list(self.discrepancies),
            "verification_complete": self.verification_complete,
            "verification_actors": sorted(self.verification_actors),
            "high_risk": self.high_risk,
            "recommendation": self.recommend().value,
            "events": list(self.events),
        }


if __name__ == "__main__":
    from role_policy import Role, WorkflowService
    case = Case("demo", {"invoice", "packing_list", "declaration"})
    workflow = WorkflowService(case)
    workflow.add_document(Role.TRADER, "invoice", actor_id="trader-1")
    workflow.add_document(Role.TRADER, "packing_list", actor_id="trader-1")
    print(case.evidence_packet())
