from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from exim_copilot_core import Case


class Role(str, Enum):
    TRADER = "trader"
    BROKER = "broker"
    FREIGHT_FORWARDER = "freight_forwarder"
    LOGISTICS_OPERATOR = "logistics_operator"
    REVIEWER = "reviewer"


PERMISSIONS = {
    Role.TRADER: {"upload_document"},
    Role.BROKER: {"upload_document", "record_discrepancy"},
    Role.FREIGHT_FORWARDER: {"upload_document"},
    Role.LOGISTICS_OPERATOR: {"upload_document"},
    Role.REVIEWER: {"upload_document", "record_discrepancy", "mark_verified"},
}


class PermissionDenied(RuntimeError):
    pass


@dataclass(frozen=True)
class RolePolicy:
    def can(self, role: Role, permission: str) -> bool:
        return permission in PERMISSIONS.get(role, set())

    def require(self, role: Role, permission: str) -> None:
        if not self.can(role, permission):
            raise PermissionDenied(f"{role.value} lacks permission: {permission}")


class WorkflowService:
    def __init__(self, case: Case, policy: RolePolicy | None = None):
        self.case = case
        self.policy = policy or RolePolicy()

    def add_document(self, role: Role, kind: str) -> None:
        self.policy.require(role, "upload_document")
        self.case.add_document(kind)
        self.case.events.append(f"actor:{role.value}:upload_document")

    def add_discrepancy(self, role: Role, detail: str) -> None:
        self.policy.require(role, "record_discrepancy")
        self.case.add_discrepancy(detail)
        self.case.events.append(f"actor:{role.value}:record_discrepancy")

    def mark_verified(self, role: Role) -> None:
        self.policy.require(role, "mark_verified")
        self.case.mark_verified()
        self.case.events.append(f"actor:{role.value}:mark_verified")
