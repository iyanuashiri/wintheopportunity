from datetime import datetime
from pydantic import BaseModel, ConfigDict


class OrganizationCreate(BaseModel):
    org_name: str
    website: str | None = None
    mission_statement: str | None = None
    focus_areas: str | None = None
    target_beneficiaries: str | None = None
    background_info: str | None = None


class OrganizationUpdate(BaseModel):
    org_name: str | None = None
    website: str | None = None
    mission_statement: str | None = None
    focus_areas: str | None = None
    target_beneficiaries: str | None = None
    background_info: str | None = None


class OrganizationRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    user_id: int
    org_name: str
    website: str | None
    mission_statement: str | None
    focus_areas: str | None
    target_beneficiaries: str | None
    background_info: str | None
    created_at: datetime