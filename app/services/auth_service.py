from app.core.exceptions import EmailAlreadyExists, InvalidCredentials
from app.core.security import create_access_token, hash_password, verify_password
from app.models.schemas.user_schema import (
    LoginRequest,
    TokenResponse,
    UserCreate,
    UserResponse,
)
from app.repositories.interfaces.user_repository_interface import IUserRepository


class AuthService:
    def __init__(self, user_repo: IUserRepository) -> None:
        self.user_repo = user_repo

    def register(self, user_data: UserCreate) -> UserResponse:
        existing_user = self.user_repo.get_user_by_email(user_data.email)
        if existing_user:
            raise EmailAlreadyExists()

        password_hash = hash_password(user_data.password)
        created_user = self.user_repo.create_user(
            user_data=user_data, password_hash=password_hash
        )

        return UserResponse.model_validate(created_user)

    def login(self, login_data: LoginRequest) -> TokenResponse:
        user = self.user_repo.get_user_by_email(login_data.email)
        if not user or not verify_password(login_data.password, user.password_hash):
            raise InvalidCredentials()

        access_token = create_access_token(
            subject=str(user.id),
            extra_claims={"email": user.email},
        )

        return TokenResponse(
            access_token=access_token,
            token_type="bearer",
            user=UserResponse.model_validate(user),
        )