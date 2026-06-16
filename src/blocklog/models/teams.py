from __future__ import annotations

from datetime import datetime
from enum import Enum

from pydantic import BaseModel, Field


class TeamRole(str, Enum):
    OWNER = "owner"
    ADMIN = "admin"
    MEMBER = "member"


class BackendTeamRole(str, Enum):
    OWNER = "owner"
    LEAD = "lead"
    REVIEWER = "reviewer"
    OBSERVER = "observer"


class Team(BaseModel):
    id: str
    company_id: str
    owner_user_id: str
    created_by: str | None = None
    name: str
    slug: str
    description: str | None = None
    is_active: bool
    default_sla_minutes: int
    created_at: datetime
    updated_at: datetime
    slack_webhook_url: str | None = None
    slack_channel: str | None = None
    email_addresses: list[str] = Field(default_factory=list)
    pagerduty_integration_key: str | None = None
    ms_teams_webhook_url: str | None = None
    custom_webhook_url: str | None = None
    custom_webhook_headers: dict[str, str] = Field(default_factory=dict)
    team_metadata: dict = Field(default_factory=dict)
    current_user_is_owner: bool = False


class TeamMember(BaseModel):
    id: str
    team_id: str
    user_id: str
    role: TeamRole
    backend_role: BackendTeamRole
    is_on_call: bool
    company_id: str | None = None
    user_email: str | None = None
    user_name: str | None = None
    notification_channels: list[str] = Field(default_factory=list)
    added_by: str | None = None
    created_at: datetime | None = None


class NotifyTestResponse(BaseModel):
    results: dict[str, bool]


def normalize_team(payload: dict) -> Team:
    data = dict(payload)
    owner_user_id = data.get("owner_user_id")
    data["owner_user_id"] = "" if owner_user_id is None else str(owner_user_id)

    created_by = data.get("created_by")
    if created_by is None and owner_user_id is not None:
        created_by = owner_user_id
    data["created_by"] = None if created_by is None else str(created_by)

    return Team.model_validate(data)


def to_sdk_role(role: str) -> TeamRole:
    if role == BackendTeamRole.OWNER.value:
        return TeamRole.OWNER
    if role == BackendTeamRole.LEAD.value:
        return TeamRole.ADMIN
    return TeamRole.MEMBER


def to_backend_role(role: TeamRole) -> BackendTeamRole:
    if role == TeamRole.OWNER:
        return BackendTeamRole.OWNER
    if role == TeamRole.ADMIN:
        return BackendTeamRole.LEAD
    return BackendTeamRole.REVIEWER


def normalize_team_member(payload: dict) -> TeamMember:
    data = dict(payload)
    backend_role = BackendTeamRole(data["role"])
    data["backend_role"] = backend_role
    data["role"] = to_sdk_role(backend_role.value)
    data["user_id"] = str(data["user_id"])
    if data.get("added_by") is not None:
        data["added_by"] = str(data["added_by"])
    return TeamMember.model_validate(data)
