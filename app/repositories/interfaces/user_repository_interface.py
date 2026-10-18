from uuid import UUID
from typing import Protocol
from app.models.tables.user import User
from app.models.schemas.user_schema import UserCreate, UserUpdate


class IUserRepository(Protocol):
    def create_user(
        self, user_data: UserCreate, password_hash: str | None = None
    ) -> User:
        ...

    def get_user_by_id(self, user_id: UUID) -> User | None:
        ...

    def get_user_by_email(self, email: str) -> User | None:
        ...

    def delete_user(self, user_id: UUID) -> bool:
        ...

    def update_user(
        self, user_id: UUID, user_data: UserUpdate | dict | None = None
    ) -> User | None:
        ...
