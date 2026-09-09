from fastapi import APIRouter, HTTPException, status

from app import crud
from app.api.deps import SessionDep, CurrentUserDep
from app.schemas.organization import OrganizationRead, OrganizationUpdate

router = APIRouter(prefix="/organizations", tags=["Organizations"])


@router.get("/me/", response_model=OrganizationRead)
async def get_my_organization(
    session: SessionDep,
    current_user: CurrentUserDep,
) -> OrganizationRead:
    """Get the current user's organization profile."""
    org = crud.get_organization_by_user(session, current_user.id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return org


@router.put("/me/", response_model=OrganizationRead)
async def update_my_organization(
    org_in: OrganizationUpdate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> OrganizationRead:
    """Update the current user's organization profile."""
    org = crud.get_organization_by_user(session, current_user.id)
    if not org:
        raise HTTPException(status_code=404, detail="Organization not found")
    return crud.update_organization(session, org, org_in)