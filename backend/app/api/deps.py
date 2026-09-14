from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from sqlalchemy.orm import Session
from jwt.exceptions import InvalidTokenError

from app import crud
from app.core.config import settings
from app.core.database import get_db
from app.models.user import User
from app.core.security import decode_access_token


SessionDep = Annotated[Session, Depends(get_db)]


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login/", auto_error=False)
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=False)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        email = decode_access_token(token)
    except InvalidTokenError:
        raise credentials_exception from None

    user = crud.get_user_by_email(session, email)
    if user is None or not user.is_active:
        raise credentials_exception
    return user


CurrentUserDep = Annotated[User, Depends(get_current_user)]


def get_service_or_user(
    api_key: Annotated[str | None, Depends(api_key_header)],
    token: Annotated[str | None, Depends(oauth2_scheme)],
    session: SessionDep,
) -> User | None:
    """Authenticate either a service (via X-API-Key) or a user (via JWT).

    Returns:
        The authenticated User, or None if authenticated as a service.
    """
    # Service API key authentication
    if api_key:
        if settings.service_api_key and api_key == settings.service_api_key:
            return None  # Service identity (no specific user)
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )

    # User JWT authentication
    if token:
        return get_current_user(token, session)

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Not authenticated",
    )


ServiceOrUserDep = Annotated[User | None, Depends(get_service_or_user)]
