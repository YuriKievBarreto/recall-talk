from fastapi.testclient import TestClient


def test_register_route_success(client: TestClient):
    payload = {
        "name": "Maria Silva",
        "email": "maria@example.com",
        "password": "senhaforte123",
        "native_language": "pt-BR",
        "target_language": "en",
        "proficiency_level": "A1",
    }

    response = client.post("/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Maria Silva"
    assert data["email"] == "maria@example.com"
    assert data["proficiency_level"] == "A1"
    assert "id" in data
    assert "password" not in data
    assert "password_hash" not in data


def test_register_route_duplicate_email(client: TestClient):
    payload = {
        "name": "Joao Souza",
        "email": "joao@example.com",
        "password": "senhaforte123",
        "native_language": "pt-BR",
        "target_language": "en",
        "proficiency_level": "B1",
    }

    first_response = client.post("/auth/register", json=payload)
    assert first_response.status_code == 201

    duplicate_response = client.post("/auth/register", json=payload)
    assert duplicate_response.status_code == 409
    assert "already exists" in duplicate_response.json()["detail"].lower()


def test_register_route_validation_error(client: TestClient):
    # Payload sem o campo obrigatório 'password' e sem 'native_language'
    invalid_payload = {
        "name": "Incompleto",
        "email": "incompleto@example.com",
    }

    response = client.post("/auth/register", json=invalid_payload)
    assert response.status_code == 422


def test_login_route_success(client: TestClient):
    register_payload = {
        "name": "Carlos Lima",
        "email": "carlos@example.com",
        "password": "minhasenhasecreta",
        "native_language": "pt-BR",
        "target_language": "es",
        "proficiency_level": "A2",
    }
    register_res = client.post("/auth/register", json=register_payload)
    assert register_res.status_code == 201

    login_payload = {
        "email": "carlos@example.com",
        "password": "minhasenhasecreta",
    }
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
    assert data["user"] is not None
    assert data["user"]["email"] == "carlos@example.com"


def test_login_route_wrong_password(client: TestClient):
    register_payload = {
        "name": "Ana Paula",
        "email": "ana@example.com",
        "password": "senhacorreta",
        "native_language": "pt-BR",
        "target_language": "en",
        "proficiency_level": "C1",
    }
    client.post("/auth/register", json=register_payload)

    login_payload = {
        "email": "ana@example.com",
        "password": "senhaincorreta",
    }
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"
    assert "invalid" in response.json()["detail"].lower()


def test_login_route_unregistered_email(client: TestClient):
    login_payload = {
        "email": "naoexiste@example.com",
        "password": "qualquersenha",
    }
    response = client.post("/auth/login", json=login_payload)

    assert response.status_code == 401
    assert response.headers.get("WWW-Authenticate") == "Bearer"


def test_login_route_validation_error(client: TestClient):
    # Sem passar o campo 'password'
    invalid_payload = {
        "email": "carlos@example.com",
    }
    response = client.post("/auth/login", json=invalid_payload)
    assert response.status_code == 422
