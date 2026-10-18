from datetime import datetime, timezone
from uuid import UUID, uuid4
import jwt
import pytest

from app.core.config import settings
from app.core.exceptions import EmailAlreadyExists, InvalidCredentials
from app.core.security import hash_password, verify_password
from app.models.schemas.user_schema import LoginRequest, TokenResponse, UserCreate, UserResponse, UserUpdate
from app.models.tables.user import ProficiencyLevel, User
from app.repositories.interfaces.user_repository_interface import IUserRepository
from app.services.auth_service import AuthService


class FakeUserRepository:
    def __init__(self):
        self.users: dict[str, User] = {}
        self.create_called = False

    def get_user_by_email(self, email: str) -> User | None:
        return self.users.get(email)

    def get_user_by_id(self, user_id: UUID) -> User | None:
        for user in self.users.values():
            if user.id == user_id:
                return user
        return None

    def create_user(
        self, user_data: UserCreate, password_hash: str | None = None
    ) -> User:
        self.create_called = True
        user = User(
            id=uuid4(),
            name=user_data.name,
            email=user_data.email,
            native_language=user_data.native_language,
            target_language=user_data.target_language,
            proficiency_level=user_data.proficiency_level,
            password_hash=password_hash or user_data.password,
            created_at=datetime.now(timezone.utc),
            is_active=True,
        )
        self.users[user.email] = user
        return user

    def delete_user(self, user_id: UUID) -> bool:
        for email, user in list(self.users.items()):
            if user.id == user_id:
                del self.users[email]
                return True
        return False

    def update_user(
        self, user_id: UUID, user_data: UserUpdate | dict | None = None
    ) -> User | None:
        user = self.get_user_by_id(user_id)
        return user


def test_register_success():
    repo = FakeUserRepository()
    service = AuthService(user_repo=repo)

    user_data = UserCreate(
        name="Lucas",
        email="lucas@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A1,
        password="plainpassword123",
    )

    response = service.register(user_data)

    assert isinstance(response, UserResponse)
    assert response.name == "Lucas"
    assert response.email == "lucas@example.com"
    assert not hasattr(response, "password_hash")

    # Verifica que a senha foi gravada hasheada
    stored_user = repo.users["lucas@example.com"]
    assert stored_user.password_hash != "plainpassword123"
    assert verify_password("plainpassword123", stored_user.password_hash) is True


def test_register_duplicate_email_raises_exception():
    repo = FakeUserRepository()
    service = AuthService(user_repo=repo)

    existing_user_data = UserCreate(
        name="Existing",
        email="duplicate@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A1,
        password="secretpassword",
    )
    service.register(existing_user_data)

    repo.create_called = False

    # Tenta registrar com o mesmo email
    with pytest.raises(EmailAlreadyExists) as exc_info:
        service.register(existing_user_data)

    assert exc_info.value.status_code == 409
    assert repo.create_called is False


def test_login_success():
    repo = FakeUserRepository()
    service = AuthService(user_repo=repo)

    # Cria o usuário previamente com senha hasheada
    user_data = UserCreate(
        name="Mariana",
        email="mariana@example.com",
        native_language="pt-BR",
        target_language="es",
        proficiency_level=ProficiencyLevel.B1,
        password="correctpassword",
    )
    service.register(user_data)

    login_req = LoginRequest(
        email="mariana@example.com", password="correctpassword"
    )
    token_response = service.login(login_req)

    assert isinstance(token_response, TokenResponse)
    assert token_response.token_type == "bearer"
    assert token_response.user is not None
    assert token_response.user.email == "mariana@example.com"

    # Valida payload do JWT
    payload = jwt.decode(
        token_response.access_token,
        settings.JWT_SECRET_KEY,
        algorithms=[settings.JWT_ALGORITHM],
    )
    assert payload["email"] == "mariana@example.com"
    assert "sub" in payload


def test_login_wrong_password_raises_invalid_credentials():
    repo = FakeUserRepository()
    service = AuthService(user_repo=repo)

    user_data = UserCreate(
        name="Pedro",
        email="pedro@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A2,
        password="rightpassword",
    )
    service.register(user_data)

    login_req = LoginRequest(
        email="pedro@example.com", password="wrongpassword"
    )
    with pytest.raises(InvalidCredentials) as exc_info:
        service.login(login_req)

    assert exc_info.value.status_code == 401


def test_login_unregistered_email_raises_invalid_credentials():
    repo = FakeUserRepository()
    service = AuthService(user_repo=repo)

    login_req = LoginRequest(
        email="nobody@example.com", password="anypassword"
    )
    with pytest.raises(InvalidCredentials) as exc_info:
        service.login(login_req)

    assert exc_info.value.status_code == 401
