from uuid import UUID
from sqlmodel import Session
from app.models.tables.user import User
from app.models.schemas.user_schema import UserCreate, UserUpdate
from app.repositories.interfaces.user_repository_interface import IUserRepository


class UserRepository(IUserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, user_data: UserCreate) -> User:
        user = User(
            name=user_data.name,
            email=user_data.email,
            native_language=user_data.native_language,
            target_language=user_data.target_language,
            proficiency_level=user_data.proficiency_level,
            password_hash=user_data.password,
        )

        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_user_by_id(self, user_id: UUID) -> User | None:
        return self.session.get(User, user_id)

    def delete_user(self, user_id: UUID) -> bool:
        user = self.get_user_by_id(user_id)
        if not user:
            return False

        self.session.delete(user)
        self.session.commit()
        return True

    def update_user(
        self, user_id: UUID, user_data: UserUpdate | dict | None = None
    ) -> User | None:
        user = self.get_user_by_id(user_id)
        if not user:
            return None

        if user_data:
            if isinstance(user_data, UserUpdate):
                update_dict = user_data.model_dump(exclude_unset=True)
            elif isinstance(user_data, dict):
                update_dict = user_data
            else:
                update_dict = {}

            # Se vier uma nova senha para atualizar, mapeia para password_hash
            if "password" in update_dict:
                update_dict["password_hash"] = update_dict.pop("password")

            for field, value in update_dict.items():
                if hasattr(user, field):
                    setattr(user, field, value)

            self.session.add(user)
            self.session.commit()
            self.session.refresh(user)

        return user
