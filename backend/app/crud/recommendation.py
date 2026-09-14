from sqlalchemy.orm import Session

from app.models.opportunity import Recommendation
from app.schemas.recommendation import RecommendationCreate


def create_recommendation(
    session: Session, rec_in: RecommendationCreate
) -> Recommendation:
    db_rec = Recommendation(
        user_id=rec_in.user_id,
        opportunity_id=rec_in.opportunity_id,
        relevance_score=rec_in.relevance_score,
        match_reason=rec_in.match_reason,
        source=rec_in.source,
    )
    session.add(db_rec)
    session.commit()
    session.refresh(db_rec)
    return db_rec


def get_recommendations_for_user(
    session: Session, user_id: int, skip: int = 0, limit: int = 50
) -> list[Recommendation]:
    return (
        session.query(Recommendation)
        .filter(Recommendation.user_id == user_id, Recommendation.is_active.is_(True))
        .order_by(Recommendation.relevance_score.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_all_recommendations(
    session: Session, skip: int = 0, limit: int = 500
) -> list[Recommendation]:
    """Get all active recommendations across all users.

    Used by the application-scraper agent to process every recommendation.
    """
    return (
        session.query(Recommendation)
        .filter(Recommendation.is_active.is_(True))
        .order_by(Recommendation.relevance_score.desc())
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_recommended_opportunity_ids(session: Session, user_id: int) -> set[int]:
    """Get the set of opportunity IDs already recommended to a user."""
    rows = (
        session.query(Recommendation.opportunity_id)
        .filter(Recommendation.user_id == user_id)
        .all()
    )
    return {row[0] for row in rows}