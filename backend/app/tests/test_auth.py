def test_register_user_success(client):
    """Успешная регистрация нового пользователя"""
    payload = {
        "email": "testuser@example.com",
        "username": "testuser",
        "password": "strongpassword123"
    }
    response = client.post("/api/auth/register", json=payload)
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert data["username"] == payload["username"]
    assert "id" in data
    assert "password" not in data

def test_register_user_duplicate_email(client):
    """Ошибка при регистрации с уже существующим email"""
    payload = {
        "email": "same@example.com",
        "username": "user1",
        "password": "password123"
    }
    client.post("/api/auth/register", json=payload)
    
    payload["username"] = "user2"
    response = client.post("/api/auth/register", json=payload)
    
    assert response.status_code == 400
    assert response.json()["detail"] == "Email уже зарегистрирован"

def test_login_success(client):
    """Успешный вход и получение JWT-токена"""
    register_payload = {
        "email": "login@example.com",
        "username": "loginuser",
        "password": "my_secret_password"
    }
    client.post("/api/auth/register", json=register_payload)

    login_data = {
        "username": "login@example.com",
        "password": "my_secret_password"
    }
    response = client.post("/api/auth/login", data=login_data)
    
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_wrong_password(client):
    """Ошибка при вводе неверного пароля"""
    register_payload = {
        "email": "wrongpwd@example.com",
        "username": "wronguser",
        "password": "correct_password"
    }
    client.post("/api/auth/register", json=register_payload)

    login_data = {
        "username": "wrongpwd@example.com",
        "password": "false_password"
    }
    response = client.post("/api/auth/login", data=login_data)
    
    assert response.status_code == 401
    assert response.json()["detail"] == "Неверный email/username или пароль"