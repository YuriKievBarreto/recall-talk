from typing import Annotated
from fastapi import APIRouter, Depends, status

from app.dependencies.service_dependencies import get_auth_service
from app.models.schemas.user_schema import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.services.auth_service import AuthService

router = APIRouter()

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]


@router.post(
    "/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED
)
def register(user_data: UserCreate, auth_service: AuthServiceDep):
    return auth_service.register(user_data)


@router.post(
    "/login", response_model=TokenResponse, status_code=status.HTTP_200_OK
)


def login(login_request: LoginRequest, auth_service: AuthServiceDep):
    return auth_service.login(login_request)