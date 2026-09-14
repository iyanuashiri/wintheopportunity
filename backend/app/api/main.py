from fastapi import APIRouter

from app.api.routes import (
    users,
    login,
    organizations,
    applications,
    opportunities,
    recommendations,
    onboarding,
)


api_router = APIRouter()

api_router.include_router(users.router)
api_router.include_router(login.router)
api_router.include_router(organizations.router)
api_router.include_router(applications.router)
api_router.include_router(opportunities.router)
api_router.include_router(recommendations.router)
api_router.include_router(onboarding.router)
