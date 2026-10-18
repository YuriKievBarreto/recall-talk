from app.core.exceptions import EmailAlreadyExists
from app.core.security import hash_password
from app.models.schemas.user_schema import UserCreate, UserResponse
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

    def login(self):
        ...