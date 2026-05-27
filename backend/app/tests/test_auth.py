def test_register_user_success(client):
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "strongpassword123",
    }
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert "id" in data
    assert "password" not in data


def test_register_user_duplicate_email(client):
    payload = {
        "email": "same@example.com",
        "username": "user1",
        "password": "password123",
    }
    client.post("/api/auth/register", json=payload)

    payload["username"] = "user2"
    response = client.post("/api/auth/register", json=payload)

    assert response.status_code == 400
    assert response.json()["detail"] == "Email уже зарегистрирован"


def test_login_success(client):
    register_payload = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "my_secret_password",
    }
    client.post("/api/auth/register", json=register_payload)

    login_data = {
        "username": "login@example.com",
        "password": "my_secret_password",
    }
    response = client.post("/api/auth/login", data=login_data)

    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client):
    register_payload = {
        "email": "wrongpwd@example.com",
        "username": "wronguser",
        "password": "correct_password",
    }
    client.post("/api/auth/register", json=register_payload)

    login_data = {
        "username": "wrongpwd@example.com",
        "password": "false_password",
    }
    response = client.post("/api/auth/login", data=login_data)

    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный email/username или пароль"


def test_me_returns_role(client):
    client.post(
        "/api/auth/register",
        json={
            "email": "me@example.com",
            "username": "meuser",
            "password": "password123",
        },
    )
    login = client.post(
        "/api/auth/login",
        data={"username": "me@example.com", "password": "password123"},
    )
    token = login.json()["access_token"]

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "meuser"
    assert data["role_name"] == "user"
    assert data["is_active"] is True


def test_blocked_user_cannot_use_token(client, db_session):
    from app.models.user import User, Role
    from app.core.security import hash_password

    role = db_session.query(Role).filter(Role.name == "user").first()
    user = User(
        email="blocked@example.com",
        username="blocked",
        password_hash=hash_password("password123"),
        role_id=role.id,
        is_active=False,
    )
    db_session.add(user)
    db_session.commit()

    login = client.post(
        "/api/auth/login",
        data={"username": "blocked@example.com", "password": "password123"},
    )
    assert login.status_code == 403

    from app.core.security import create_access_token

    token = create_access_token({"sub": "blocked@example.com"})
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 403
