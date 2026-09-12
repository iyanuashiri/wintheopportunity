from sqlalchemy.orm import Session

from app.models.organization import Organization
from app.schemas.organization import OrganizationCreate, OrganizationUpdate


def get_organization_by_user(session: Session, user_id: int) -> Organization | None:
    return session.query(Organization).filter(Organization.user_id == user_id).first()


def get_all_organizations(
    session: Session, skip: int = 0, limit: int = 100
) -> list[Organization]:
    return (
        session.query(Organization)
        .order_by(Organization.created_at.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def update_organization(
    session: Session, db_org: Organization, org_in: OrganizationUpdate
) -> Organization:
    data = org_in.model_dump(exclude_unset=True)
    for field, value in data.items():
        setattr(db_org, field, value)
    session.commit()
    session.refresh(db_org)
    return db_org