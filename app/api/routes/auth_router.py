from fastapi import APIRouter
from app.models.schemas.user_schema import UserCreate, UserResponse
from fastapi import Depends, status
from app.dependencies.service_dependencies import get_auth_service
from app.services.auth_service import AuthService
from typing import Annotated

router = APIRouter()

AuthServiceDep = Annotated[AuthService, Depends(get_auth_service)]

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register(user_data: UserCreate, auth_service: AuthServiceDep):
    return auth_service.register(user_data)
     