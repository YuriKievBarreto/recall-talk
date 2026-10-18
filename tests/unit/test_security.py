from datetime import datetime, timedelta, timezone
import jwt
from app.core.config import settings
from app.core.security import create_access_token, hash_password, verify_password


def test_hash_password_generates_valid_bcrypt_hash():
    password = "minhasenha123"
    hashed = hash_password(password)

    assert hashed != password
    assert hashed.startswith("$2b$")


def test_hash_password_generates_unique_salts():
    password = "mesmasenha"
    hash1 = hash_password(password)
    hash2 = hash_password(password)

    assert hash1 != hash2


def test_verify_password_success():
    password = "secretpassword"
    hashed = hash_password(password)

    assert verify_password(password, hashed) is True


def test_verify_password_failure():
    password = "secretpassword"
    wrong_password = "wrongpassword"
    hashed = hash_password(password)

    assert verify_password(wrong_password, hashed) is False


def test_create_access_token_contains_expected_claims():
    subject = "user-id-123"
    extra = {"email": "test@example.com"}

    token = create_access_token(subject=subject, extra_claims=extra)
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )

    assert payload["sub"] == subject
    assert payload["email"] == "test@example.com"
    assert "exp" in payload
    assert payload["exp"] > datetime.now(timezone.utc).timestamp()


def test_create_access_token_respects_custom_expiry():
    subject = "user-id-456"
    custom_delta = timedelta(minutes=15)

    token = create_access_token(subject=subject, expires_delta=custom_delta)
    payload = jwt.decode(
        token, settings.JWT_SECRET_KEY, algorithms=[settings.JWT_ALGORITHM]
    )

    now_ts = datetime.now(timezone.utc).timestamp()
    expected_expiry = now_ts + (15 * 60)
    # Tolerância de 5 segundos
    assert abs(payload["exp"] - expected_expiry) < 5
