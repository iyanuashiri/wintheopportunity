from fastapi import APIRouter, HTTPException, status

from app.api.deps import SessionDep, CurrentUserDep, ServiceOrUserDep
from app.crud import application as crud_application
from app.schemas.application import (
    ApplicationCreate,
    ApplicationReadSummary,
    ApplicationReadDetail,
    ImageCreate,
    ImageRead,
)

router = APIRouter(prefix="/applications", tags=["Applications"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ApplicationReadDetail)
async def create_application(
    application_in: ApplicationCreate,
    session: SessionDep,
    current_user: ServiceOrUserDep,
) -> ApplicationReadDetail:
    """Create a new application along with initial questions/answers if provided.

    Accepts either a user JWT or a service API key (for the application-scraper agent).
    """
    user_id = current_user.id if current_user else application_in.user_id
    return crud_application.create_application(session, application_in, user_id)


@router.post("/{application_id}/images/", status_code=status.HTTP_201_CREATED, response_model=ImageRead)
async def create_application_image(
    application_id: int,
    image_in: ImageCreate,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ImageRead:
    """Upload a screenshot image for an application (one at a time)."""
    application = crud_application.get_application_by_id(session, application_id, current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return crud_application.create_image(session, application_id, image_in)


@router.get("/", response_model=list[ApplicationReadSummary])
async def list_applications(
    session: SessionDep,
    current_user: CurrentUserDep,
    skip: int = 0,
    limit: int = 20,
) -> list[ApplicationReadSummary]:
    """List all applications created by the user (Commonly Answered Questions backlog)."""
    return crud_application.get_user_applications(session, current_user.id, skip=skip, limit=limit)


@router.get("/{application_id}/", response_model=ApplicationReadDetail)
async def get_application_detail(
    application_id: int,
    session: SessionDep,
    current_user: CurrentUserDep,
) -> ApplicationReadDetail:
    """Get full details of a specific application including questions, answers, and evaluations."""
    application = crud_application.get_application_by_id(session, application_id, current_user.id)
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application