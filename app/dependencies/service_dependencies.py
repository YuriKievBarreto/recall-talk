from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.services.auth_service import AuthService
from app.dependencies.repo_dependencies import get_user_repository
from fastapi import Depends


def get_auth_service(
    user_repo: IUserRepository = Depends(get_user_repository),
) -> AuthService:
    return AuthService(user_repo=user_repo)