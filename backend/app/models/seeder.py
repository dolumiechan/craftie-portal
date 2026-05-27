from datetime import datetime, timezone
from typing import Optional

from sqlalchemy.orm import Session

from app.core.database import SessionLocal
from app.core.security import get_password_hash
from app.models.user import User, Role
from app.models.post import Post, PostImage
from app.models.category import InterestCategory as Category
from app.models.tag import Tag

PINTEREST_IMAGES = [
    "https://i.pinimg.com/736x/1c/c9/d8/1cc9d8bc553565bbd47f7dac50ebbd08.jpg",        # 1. Торт крючком
    "https://i.pinimg.com/736x/67/00/a4/6700a475a406e93479db15452d37b47e.jpg",         # 2. Заколка печенье
    "https://i.pinimg.com/736x/15/a8/6c/15a86ca939ec56ea439423305a2ce323.jpg",             # 3. Тортик из бисера
    "https://i.pinimg.com/1200x/74/57/68/74576869038de47e04fdd4465bf2dc9a.jpg",           # 4. Чехол decoden
    "https://i.pinimg.com/736x/8e/2a/47/8e2a470d4803605edd1a6b14782e6011.jpg",             # 5. Скетч игрушек
    "https://i.pinimg.com/736x/a0/e1/e1/a0e1e139d25193e342d1db4c37df2464.jpg",   # 6. Headdress decoden
    "https://i.pinimg.com/736x/cc/62/5d/cc625da8605a22564dd7fd549652d544.jpg",              # 7. Веб-дизайн
    "https://i.pinimg.com/1200x/3e/c8/0f/3ec80fe5d93140b09715cbf8ca2b2a2b.jpg",              # 8. Cyberdeck
    "https://i.pinimg.com/1200x/9d/83/dc/9d83dce07d6cac0770ba5736f3933b4d.jpg",          # 9. Брелок из глины
    "https://i.pinimg.com/474x/0a/a7/5e/0aa75ebb603854fe712a1b562cb38170.jpg"            # 10. Thrift flip топ
]

ROLE_DEFINITIONS = (
    (1, "user"),
    (2, "moderator"),
    (3, "admin"),
)

def _password_field_kwargs(hashed_password: str) -> dict:
    if hasattr(User, "hashed_password"):
        return {"hashed_password": hashed_password}
    if hasattr(User, "password_hash"):
        return {"password_hash": hashed_password}
    if hasattr(User, "password"):
        return {"password": hashed_password}
    return {"password_hash": hashed_password}

def _seed_roles(db: Session) -> None:
    if db.query(Role).first():
        return

    db.add_all(Role(id=role_id, name=name) for role_id, name in ROLE_DEFINITIONS)
    db.flush()

def seed_data(db: Optional[Session] = None):
    if db is None:
        db = SessionLocal()
        should_close = True
    else:
        should_close = False

    try:
        print("Начало наполнения базы данных администраторами и творческими проектами...")

        categories_data = [
            "Вязание", "Аксессуары", "Бисероплетение", "Decoden", "Рисование",
            "Шитье", "Веб-дизайн", "Электроника & DIY", "Лепка", "Кастомизация одежды"
        ]
        categories = {}
        for cat_name in categories_data:
            cat = db.query(Category).filter(Category.name == cat_name).first()
            if not cat:
                cat = Category(name=cat_name)
                db.add(cat)
                db.flush()
            categories[cat_name] = cat

        tags_data = ["handmade", "korilakkuma", "felt", "beads", "y2k", "aesthetic", "cyberpunk", "raspberrypi", "clay", "thriftflip", "kawaii"]
        tags = {}
        for t_name in tags_data:
            tag = db.query(Tag).filter(Tag.name == t_name).first()
            if not tag:
                tag = Tag(name=t_name)
                db.add(tag)
                db.flush()
            tags[t_name] = tag

        _seed_roles(db)

        password_kwargs = _password_field_kwargs(get_password_hash("password123"))

        staff_data = [
                {
                    "username": "admin", 
                    "email": "admin@creative.me", 
                    "bio": "Главный администратор платформы. Управление категориями и пользователями.", 
                    "role_id": 3
                },
                {
                    "username": "moderator_owl", 
                    "email": "mod@creative.me", 
                    "bio": "Модератор сообщества. Слежу за порядком, красотой и соблюдением правил.", 
                    "role_id": 2
                }
            ]

        authors_data = [
                {"username": "yarn_fairy", "email": "fairy@craft.me", "bio": "Вяжу уютные игрушки и сладости крючком.", "role_id": 1},
                {"username": "felt_artisan", "email": "felt@craft.me", "bio": "Создаю милые аксессуары из фетра и ткани.", "role_id": 1},
                {"username": "bead_master", "email": "beads@craft.me", "bio": "Плету из бисера сложные миниатюры и схемы.", "role_id": 1},
                {"username": "sweet_decoden", "email": "deco@craft.me", "bio": "Покрываю этот мир искусственным крем-клеем.", "role_id": 1},
                {"username": "nostalgia_draw", "email": "sketch@craft.me", "bio": "Иллюстратор, влюбленный в игрушки нашего детства.", "role_id": 1},
                {"username": "lolita_sewing", "email": "sew@craft.me", "bio": "Шью хеддрессы и платья в стиле J-fashion.", "role_id": 1},
                {"username": "rilakkuma_designer", "email": "design@craft.me", "bio": "UI/UX дизайнер. Делаю интерфейсы милыми.", "role_id": 1},
                {"username": "cyber_trash", "email": "pi@craft.me", "bio": "Собираю портативные ПК из старого хлама и Raspberry Pi.", "role_id": 1},
                {"username": "clay_bakery", "email": "clay@craft.me", "bio": "Миниатюрная кулинария из полимерной глины.", "role_id": 1},
                {"username": "thrift_queen", "email": "flip@craft.me", "bio": "Даю старым вещам вторую жизнь!", "role_id": 1}
            ]

        all_users = staff_data + authors_data
        users_dict = {}

        for u_info in all_users:
            user = db.query(User).filter(User.username == u_info["username"]).first()
            if not user:
                user = User(
                    username=u_info["username"],
                    email=u_info["email"],
                    bio=u_info["bio"],
                    is_active=True,
                    role_id=u_info["role_id"],
                    **password_kwargs,
                )
                db.add(user)
                db.flush()
            users_dict[u_info["username"]] = user

        users = [users_dict[auth["username"]] for auth in authors_data]

        # 5. Данные для 10 творческих постов
        posts_data = [
                {
                    "title": "Вязаный торт крючком с Корилаккумой",
                    "description": "Мой новый проект! Это объемный праздничный торт, полностью связанный крючком из нежной пряжи. Сверху красуется Корилаккума!",
                    "cat": "Вязание",
                    "img": PINTEREST_IMAGES[0],
                    "post_tags": ["handmade", "korilakkuma", "kawaii"],
                    "author_idx": 0
                },
                {
                    "title": "Милая заколка-печенье из мягкого фетра",
                    "description": "Сделала заколку для волос в виде реалистичного шоколадного печенья. Материал — корейский жесткий и мягкий фетр, расшитый вручную.",
                    "cat": "Аксессуары",
                    "img": PINTEREST_IMAGES[1],
                    "post_tags": ["handmade", "felt", "aesthetic"],
                    "author_idx": 1
                },
                {
                    "title": "Объемный тортик из бисера + авторская схема",
                    "description": "Плела эту миниатюру около трех дней с использованием японского бисера Toho 11/0. Делюсь своей подробной схемой плетения в описании!",
                    "cat": "Бисероплетение",
                    "img": PINTEREST_IMAGES[2],
                    "post_tags": ["handmade", "beads", "aesthetic"],
                    "author_idx": 2
                },
                {
                    "title": "Кастомный чехол Decoden со сладостями",
                    "description": "Превратила обычный прозрачный чехол в безумное кремовое облако! Использовала силиконовый крем-клей, кабошоны и кучу маршмеллоу.",
                    "cat": "Decoden",
                    "img": PINTEREST_IMAGES[3],
                    "post_tags": ["handmade", "aesthetic", "kawaii"],
                    "author_idx": 3
                },
                {
                    "title": "Ностальгический скетч: Игрушки нашего детства",
                    "description": "Погружение в 2010-е! Нарисовала маркерный скетч с любимыми игрушками: ZhuZhu Pets, Lalaloopsy, Hello Kitty, Littlest Pet Shop и крошечные Squinkies.",
                    "cat": "Рисование",
                    "img": PINTEREST_IMAGES[4],
                    "post_tags": ["y2k", "aesthetic"],
                    "author_idx": 4
                },
                {
                    "title": "Headdress Strawberry Shortcake с элементами decoden",
                    "description": "Сшила головной убор на швейной машинке из хлопка и кружева, а боковые элементы декорировала в стиле декоден со спелыми клубничками.",
                    "cat": "Шитье",
                    "img": PINTEREST_IMAGES[5],
                    "post_tags": ["handmade", "aesthetic", "kawaii"],
                    "author_idx": 5
                },
                {
                    "title": "Концепт веб-дизайна для мерч-шопа Corilakkuma",
                    "description": "Разработала пастельный, милый и интуитивный UI/UX дизайн интернет-магазина, специализирующегося на оригинальном мерче с Корилаккумой.",
                    "cat": "Веб-дизайн",
                    "img": PINTEREST_IMAGES[6],
                    "post_tags": ["korilakkuma", "kawaii"],
                    "author_idx": 6
                },
                {
                    "title": "Cyberdeck: Собрала мини-лэптоп на Arch Linux",
                    "description": "Сумасшедший DIY! Взяла старый детский игрушечный ноутбук, выпотрошила его, встроила плату Raspberry Pi, IPS-экран и накатила Arch Linux.",
                    "cat": "Электроника & DIY",
                    "img": PINTEREST_IMAGES[7],
                    "post_tags": ["cyberpunk", "raspberrypi"],
                    "author_idx": 7
                },
                {
                    "title": "Брелок «Шоколадное печенье» из полимерной глины",
                    "description": "Миниатюрная кулинария! Слепила брелок-печенье с текстурой запеченного теста и кусочками шоколада. Покрыто матовым защитным лаком.",
                    "cat": "Лепка",
                    "img": PINTEREST_IMAGES[8],
                    "post_tags": ["handmade", "clay"],
                    "author_idx": 8
                },
                {
                    "title": "Thrift Flip: Из старых розовых штанов в топ",
                    "description": "Нашла на барахолке скучные мешковатые розовые джинсы и полностью перешила их в трендовый нежный топ в стиле бэбидолл с рюшами.",
                    "cat": "Кастомизация одежды",
                    "img": PINTEREST_IMAGES[9],
                    "post_tags": ["handmade", "thriftflip", "y2k"],
                    "author_idx": 9
                }
            ]

        for p_data in posts_data:
            existing_post = db.query(Post).filter(Post.title == p_data["title"]).first()
            if not existing_post:
                new_post = Post(
                    title=p_data["title"],
                    description=p_data["description"],
                    category_id=categories[p_data["cat"]].id,
                    author_id=users[p_data["author_idx"]].id,
                    created_at=datetime.now(timezone.utc),
                )
                for t_name in p_data["post_tags"]:
                    new_post.tags.append(tags[t_name])

                db.add(new_post)
                db.flush()
                db.add(PostImage(post_id=new_post.id, image_url=p_data["img"]))

        db.commit()
        print("База данных успешно заполнена! Созданы Admin, Moderator, 10 авторов и 10 постов.")
    except Exception as e:
        db.rollback()
        print(f"Ошибка при заполнении сидера: {e}")
    finally:
        if should_close:
            db.close()


if __name__ == "__main__":
    seed_data()