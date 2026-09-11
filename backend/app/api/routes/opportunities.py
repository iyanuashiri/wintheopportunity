from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep
from app.crud import opportunity as crud_opportunity
from app.models.opportunity import Opportunity
from app.schemas.opportunity import (
    OpportunityCreate,
    OpportunityRead,
    OpportunityUpsertResult,
)

router = APIRouter(prefix="/opportunities", tags=["Opportunities"])


@router.get("/", response_model=list[OpportunityRead])
async def list_opportunities(
    session: SessionDep,
    skip: int = 0,
    limit: int = 100,
) -> list[OpportunityRead]:
    """List all scraped opportunities."""
    return crud_opportunity.get_all_opportunities(session, skip=skip, limit=limit)


@router.get("/{opportunity_id}/", response_model=OpportunityRead)
async def get_opportunity(
    opportunity_id: int,
    session: SessionDep,
) -> OpportunityRead:
    """Get a single opportunity by id."""
    opp = session.get(Opportunity, opportunity_id)
    if not opp:
        raise HTTPException(status_code=404, detail="Opportunity not found")
    return opp


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=OpportunityRead)
async def create_opportunity(
    opp_in: OpportunityCreate,
    session: SessionDep,
) -> OpportunityRead:
    """Create a single opportunity."""
    opp = Opportunity(**opp_in.model_dump())
    return crud_opportunity.create_opportunity(session, opp)


@router.post("/upsert/", response_model=OpportunityUpsertResult)
async def upsert_opportunities(
    opportunities: list[OpportunityCreate],
    session: SessionDep,
) -> OpportunityUpsertResult:
    """Bulk upsert opportunities by composite key. Used by the scraper agent."""
    created = 0
    updated = 0
    saved: list[Opportunity] = []
    for data in opportunities:
        opp = Opportunity(**data.model_dump())
        existing = crud_opportunity.get_opportunity_by_url(
            session, opp.opportunity_url, opp.start_date, opp.deadline
        )
        if existing:
            updated += 1
        else:
            created += 1
        saved.append(crud_opportunity.upsert_opportunity(session, opp))
    return OpportunityUpsertResult(created=created, updated=updated, opportunities=saved)