from app.models.category import InterestCategory
from app.models.post import Post, PostImage
from app.models.user import User, Role
from app.core.security import hash_password


def _create_user(db, username="author", email="author@test.com"):
    role = db.query(Role).filter(Role.name == "user").first()
    user = User(
        username=username,
        email=email,
        password_hash=hash_password("password123"),
        role_id=role.id,
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


def _create_post(db, user, title, description=None, category=None):
    post = Post(
        title=title,
        description=description,
        author_id=user.id,
        category_id=category.id if category else None,
    )
    db.add(post)
    db.flush()
    db.add(PostImage(post_id=post.id, image_url="/media/test.jpg"))
    db.commit()
    db.refresh(post)
    return post


def test_list_posts_empty(client):
    response = client.get("/api/posts/")
    assert response.status_code == 200
    data = response.json()
    assert data["items"] == []
    assert data["total"] == 0


def test_list_posts_search(client, db_session):
    user = _create_user(db_session)
    _create_post(db_session, user, "Керамическая ваза", "Ручная лепка из глины")
    _create_post(db_session, user, "Музыкальный этюд", "Фортепиано")

    response = client.get("/api/posts/", params={"search": "керамик"})
    assert response.status_code == 200
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["title"] == "Керамическая ваза"
    assert data["items"][0]["author_username"] == "author"
    assert data["items"][0]["image_url"] == "/media/test.jpg"


def test_list_posts_category_filter(client, db_session):
    user = _create_user(db_session)
    cat = InterestCategory(name="Рисование")
    db_session.add(cat)
    db_session.commit()
    db_session.refresh(cat)

    _create_post(db_session, user, "Пост A", category=cat)
    _create_post(db_session, user, "Пост B")

    response = client.get("/api/posts/", params={"category_id": cat.id})
    data = response.json()
    assert data["total"] == 1
    assert data["items"][0]["category_name"] == "Рисование"


def test_get_post_detail(client, db_session):
    user = _create_user(db_session)
    post = _create_post(db_session, user, "Детальный пост", "Описание работы")

    response = client.get(f"/api/posts/{post.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Детальный пост"
    assert data["author_username"] == "author"
    assert data["description"] == "Описание работы"
    assert data["comments_count"] == 0
