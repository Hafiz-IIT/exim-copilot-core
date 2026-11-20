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
    Role.REVIEWER: {"upload_document", "record_discrepancy", "resolve_discrepancy", "mark_verified"},
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

    def add_document(self, role: Role, kind: str, *, actor_id: str) -> None:
        self.policy.require(role, "upload_document")
        self.case._add_document(kind, actor_id)
        self.case.events.append(f"actor-role:{role.value}:upload_document")

    def add_discrepancy(self, role: Role, detail: str, *, actor_id: str) -> None:
        self.policy.require(role, "record_discrepancy")
        self.case._add_discrepancy(detail, actor_id)
        self.case.events.append(f"actor-role:{role.value}:record_discrepancy")

    def resolve_discrepancy(self, role: Role, detail: str, *, actor_id: str) -> None:
        self.policy.require(role, "resolve_discrepancy")
        self.case._resolve_discrepancy(detail, actor_id)
        self.case.events.append(f"actor-role:{role.value}:resolve_discrepancy")

    def mark_verified(self, role: Role, *, actor_id: str) -> None:
        self.policy.require(role, "mark_verified")
        self.case._record_verification(actor_id)
        self.case.events.append(f"actor-role:{role.value}:mark_verified")
