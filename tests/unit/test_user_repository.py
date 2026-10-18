from uuid import uuid4
from sqlmodel import Session

from app.models.schemas.user_schema import UserCreate, UserUpdate
from app.models.tables.user import ProficiencyLevel
from app.repositories.user_repository import UserRepository


def test_create_user_with_plain_password(session: Session):
    repo = UserRepository(session=session)
    user_data = UserCreate(
        name="Alice",
        email="alice@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A1,
        password="plain_password",
    )

    user = repo.create_user(user_data)

    assert user.id is not None
    assert user.name == "Alice"
    assert user.email == "alice@example.com"
    assert user.password_hash == "plain_password"


def test_create_user_with_custom_password_hash(session: Session):
    repo = UserRepository(session=session)
    user_data = UserCreate(
        name="Bob",
        email="bob@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A2,
        password="raw_password",
    )

    user = repo.create_user(user_data, password_hash="hashed_secret")

    assert user.id is not None
    assert user.password_hash == "hashed_secret"


def test_get_user_by_id_success(session: Session):
    repo = UserRepository(session=session)
    user_data = UserCreate(
        name="Charlie",
        email="charlie@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.B1,
        password="password123",
    )
    created = repo.create_user(user_data)

    fetched = repo.get_user_by_id(created.id)

    assert fetched is not None
    assert fetched.id == created.id
    assert fetched.email == "charlie@example.com"


def test_get_user_by_id_not_found(session: Session):
    repo = UserRepository(session=session)
    random_id = uuid4()

    assert repo.get_user_by_id(random_id) is None


def test_get_user_by_email_success(session: Session):
    repo = UserRepository(session=session)
    user_data = UserCreate(
        name="Diana",
        email="diana@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.B2,
        password="password123",
    )
    repo.create_user(user_data)

    found = repo.get_user_by_email("diana@example.com")

    assert found is not None
    assert found.name == "Diana"


def test_get_user_by_email_not_found(session: Session):
    repo = UserRepository(session=session)

    assert repo.get_user_by_email("unknown@example.com") is None


def test_update_user_fields(session: Session):
    repo = UserRepository(session=session)
    user_data = UserCreate(
        name="Eve",
        email="eve@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A1,
        password="password123",
    )
    created = repo.create_user(user_data)

    update_data = UserUpdate(
        name="Eve Updated",
        proficiency_level=ProficiencyLevel.C1,
    )
    updated = repo.update_user(created.id, update_data)

    assert updated is not None
    assert updated.name == "Eve Updated"
    assert updated.proficiency_level == ProficiencyLevel.C1
    assert updated.email == "eve@example.com"


def test_update_user_password(session: Session):
    repo = UserRepository(session=session)
    user_data = UserCreate(
        name="Frank",
        email="frank@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A1,
        password="old_password",
    )
    created = repo.create_user(user_data)

    update_data = UserUpdate(password="new_password_hash")
    updated = repo.update_user(created.id, update_data)

    assert updated is not None
    assert updated.password_hash == "new_password_hash"


def test_update_user_not_found(session: Session):
    repo = UserRepository(session=session)
    random_id = uuid4()

    result = repo.update_user(random_id, UserUpdate(name="Nonexistent"))
    assert result is None


def test_delete_user_success(session: Session):
    repo = UserRepository(session=session)
    user_data = UserCreate(
        name="Grace",
        email="grace@example.com",
        native_language="pt-BR",
        target_language="en",
        proficiency_level=ProficiencyLevel.A1,
        password="password123",
    )
    created = repo.create_user(user_data)

    deleted = repo.delete_user(created.id)

    assert deleted is True
    assert repo.get_user_by_id(created.id) is None


def test_delete_user_not_found(session: Session):
    repo = UserRepository(session=session)
    random_id = uuid4()

    assert repo.delete_user(random_id) is False
