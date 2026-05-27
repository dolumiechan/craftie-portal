from app.models.category import InterestCategory
from app.models.user import User, Role
from app.core.security import hash_password, create_access_token


def _auth_headers(db, email="profile@test.com", username="profileuser"):
    role = db.query(Role).filter(Role.name == "user").first()
    user = User(
        email=email,
        username=username,
        password_hash=hash_password("password123"),
        role_id=role.id,
        bio="Старое bio",
    )
    db.add(user)
    db.commit()
    token = create_access_token({"sub": email})
    return {"Authorization": f"Bearer {token}"}, user


def test_get_profile_with_bio(client, db_session):
    headers, user = _auth_headers(db_session)
    response = client.get("/api/profile/", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Старое bio"
    assert data["username"] == user.username


def test_update_profile_bio_and_interests(client, db_session):
    headers, user = _auth_headers(db_session, "upd@test.com", "upduser")
    cat = InterestCategory(name="Музыка")
    db_session.add(cat)
    db_session.commit()

    response = client.put(
        "/api/profile/",
        headers=headers,
        data={
            "username": "upduser",
            "email": "upd@test.com",
            "bio": "Новое описание автора",
            "interest_ids": f"[{cat.id}]",
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["bio"] == "Новое описание автора"
    assert len(data["interests"]) == 1
    assert data["interests"][0]["name"] == "Музыка"


def test_profile_comments_history(client, db_session):
    from app.models.post import Post
    from app.models.comment import Comment

    headers, user = _auth_headers(db_session, "comm@test.com", "commuser")
    post = Post(title="Работа для комментария", author_id=user.id)
    db_session.add(post)
    db_session.flush()
    db_session.add(
        Comment(post_id=post.id, user_id=user.id, text="Мой первый отзыв")
    )
    db_session.commit()

    response = client.get("/api/profile/comments", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["post_title"] == "Работа для комментария"
    assert data[0]["text"] == "Мой первый отзыв"
