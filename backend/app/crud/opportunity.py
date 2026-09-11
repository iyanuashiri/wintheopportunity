from datetime import datetime

from sqlalchemy.orm import Session

from app.models.opportunity import Opportunity


def get_opportunity_by_url(
    session: Session,
    opportunity_url: str,
    start_date: datetime | None,
    deadline: datetime | None,
) -> Opportunity | None:
    """Find an opportunity by its composite unique key.

    An opportunity is uniquely identified by its landing page URL combined
    with its start date and deadline. The same URL can be reused yearly
    (the page content changes), so URL alone is not unique.
    """
    return (
        session.query(Opportunity)
        .filter(
            Opportunity.opportunity_url == opportunity_url,
            Opportunity.start_date == start_date,
            Opportunity.deadline == deadline,
        )
        .first()
    )


def create_opportunity(session: Session, opportunity: Opportunity) -> Opportunity:
    session.add(opportunity)
    session.commit()
    session.refresh(opportunity)
    return opportunity


def upsert_opportunity(session: Session, opportunity: Opportunity) -> Opportunity:
    """Insert a new opportunity or update an existing one by composite key."""
    existing = get_opportunity_by_url(
        session,
        opportunity.opportunity_url,
        opportunity.start_date,
        opportunity.deadline,
    )
    if existing:
        for field, value in opportunity.__dict__.items():
            if field.startswith("_") or value is None:
                continue
            setattr(existing, field, value)
        session.commit()
        session.refresh(existing)
        return existing
    return create_opportunity(session, opportunity)


def get_all_opportunities(session: Session, skip: int = 0, limit: int = 100) -> list[Opportunity]:
    return (
        session.query(Opportunity)
        .order_by(Opportunity.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )