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

    def add_document(self, kind: str) -> None:
        self.received_documents.add(kind)
        self.events.append(f"document:{kind}")

    def add_discrepancy(self, detail: str) -> None:
        self.discrepancies.append(detail)
        self.events.append(f"discrepancy:{detail}")

    def mark_verified(self) -> None:
        self.verification_complete = True
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
            "high_risk": self.high_risk,
            "recommendation": self.recommend().value,
            "events": list(self.events),
        }


if __name__ == "__main__":
    case = Case("demo", {"invoice", "packing_list", "declaration"})
    case.add_document("invoice")
    case.add_document("packing_list")
    print(case.evidence_packet())
