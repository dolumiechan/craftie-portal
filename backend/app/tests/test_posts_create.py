from app.models.user import User, Role
from app.core.security import hash_password, create_access_token


def _headers(db):
    role = db.query(Role).filter(Role.name == "user").first()
    user = User(
        email="creator@test.com",
        username="creator",
        password_hash=hash_password("password123"),
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    token = create_access_token({"sub": "creator@test.com"})
    return {"Authorization": f"Bearer {token}"}


def test_create_post_with_image(client, db_session):
    headers = _headers(db_session)
    response = client.post(
        "/api/posts/",
        headers=headers,
        data={"title": "Новая работа", "description": "Описание", "tags_json": '["керамика"]'},
        files={"file": ("test.png", b"\x89PNG\r\n\x1a\n", "image/png")},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Новая работа"
    assert data["author_username"] == "creator"
    assert data["image_url"].startswith("/media/")


def test_list_my_posts(client, db_session):
    headers = _headers(db_session)
    client.post(
        "/api/posts/",
        headers=headers,
        data={"title": "Моя работа"},
        files={"file": ("a.jpg", b"\xff\xd8\xff", "image/jpeg")},
    )
    response = client.get("/api/posts/my", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
