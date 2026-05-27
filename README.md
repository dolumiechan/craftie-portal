# Craftie Portal

Веб-платформа для публикации и обсуждения творческих работ: лента с поиском и категориями, профили авторов, лайки, комментарии и админ-панель для модерации.

| Сервис   | URL (Docker)              | URL (локальная разработка) |
|----------|---------------------------|----------------------------|
| Frontend | http://localhost:3000     | http://localhost:3000      |
| Backend  | http://localhost:8000     | http://localhost:8000      |
| API docs | http://localhost:8000/docs | http://localhost:8000/docs |

---

## Содержание

- [Возможности](#возможности)
- [Стек технологий](#стек-технологий)
- [Архитектура](#архитектура)
- [Структура проекта](#структура-проекта)
- [Требования](#требования)
- [Быстрый старт (Docker)](#быстрый-старт-docker)
- [Локальная разработка](#локальная-разработка)
- [Переменные окружения](#переменные-окружения)
- [Учётные записи по умолчанию](#учётные-записи-по-умолчанию)
- [Роли и права доступа](#роли-и-права-доступа)
- [API](#api)
- [Маршруты frontend](#маршруты-frontend)
- [Медиафайлы](#медиафайлы)
- [Тестирование](#тестирование)
- [Создание администратора вручную](#создание-администратора-вручную)
- [Устранение неполадок](#устранение-неполадок)

---

## Возможности

### Для всех пользователей
- Публичная лента публикаций с пагинацией («Показать ещё»)
- Поиск по названию и описанию
- Фильтрация по категориям интересов
- Просмотр карточки работы, автора и комментариев
- Информационные страницы: «О нас», «Помощь», «Контакты», «Мероприятия»

### Для зарегистрированных пользователей
- Регистрация и вход (JWT, Bearer-токен)
- Профиль: имя, email, bio, аватар, категории интересов
- Создание, редактирование и удаление своих публикаций
- Загрузка изображений (JPEG, PNG, WebP) с автоматическим ресайзом
- Теги к публикациям
- Лайки
- Комментарии к работам
- История своих комментариев и список своих публикаций в профиле

### Для модераторов и администраторов
- Админ-панель (`/admin`)
- Просмотр и модерация всех публикаций (скрытие / удаление)
- Управление категориями интересов (только admin)
- Управление пользователями: роли, блокировка (только admin)
- Экспорт пользователей в CSV (только admin)
- Журнал действий пользователей

---

## Стек технологий

| Слой      | Технологии |
|-----------|------------|
| Backend   | Python 3.11, FastAPI, SQLAlchemy, Pydantic v2, PostgreSQL, JWT (PyJWT), bcrypt, Pillow |
| Frontend  | React 19, Vite 8, React Router 7, Tailwind CSS v4, Axios |
| Инфра     | Docker, Docker Compose, Nginx (production frontend), Uvicorn |

База данных создаётся автоматически при старте backend (`Base.metadata.create_all`). При первом запуске выполняется сидер с демо-данными.

---

## Архитектура

```
┌─────────────┐     /api, /media      ┌─────────────┐      SQL       ┌────────────┐
│   Browser   │ ────────────────────► │   Backend   │ ◄────────────► │ PostgreSQL │
│  (React)    │                       │  (FastAPI)  │                │            │
└─────────────┘                       └──────┬──────┘                └────────────┘
                                             │
                                             ▼
                                      backend/media/
                                      (загруженные файлы)
```

**Docker:** Nginx во frontend-контейнере отдаёт статику и проксирует `/api` и `/media` на backend.

**Локально:** Vite dev server на порту 3000 проксирует `/api` и `/media` на `http://localhost:8000`.

---

## Структура проекта

```
craftie-portal/
├── backend/
│   ├── app/
│   │   ├── api/           # REST-роутеры (auth, posts, comments, likes, profile, categories, admin)
│   │   ├── core/          # config, database, security, image_service
│   │   ├── models/        # SQLAlchemy-модели и seeder
│   │   ├── schemas/       # Pydantic-схемы запросов/ответов
│   │   ├── services/      # post_feed, user_mapper, logger
│   │   ├── repositories/  # UserRepository
│   │   ├── tests/         # pytest
│   │   ├── main.py        # точка входа FastAPI
│   │   └── create_admin.py
│   ├── media/             # загруженные изображения (в .gitignore)
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── api/           # HTTP-клиенты
│   │   ├── components/    # UI-компоненты
│   │   ├── context/       # AuthContext
│   │   ├── pages/         # страницы и админка
│   │   └── utils/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
├── docker-compose.yml
├── .env.example
└── README.md
```

---

## Требования

- **Docker-вариант:** Docker Desktop / Docker Engine + Docker Compose v2
- **Локальный вариант:**
  - Python 3.11+
  - Node.js 20+
  - PostgreSQL 15+

---

## Быстрый старт (Docker)

### 1. Клонировать репозиторий

```bash
git clone <url-репозитория>
cd craftie-portal
```

### 2. Настроить окружение

```bash
cp .env.example .env
```

Откройте `.env` и задайте надёжные значения как минимум для:

- `POSTGRES_PASSWORD`
- `SECRET_KEY` (случайная строка, минимум 32 символа)

### 3. Запустить все сервисы

```bash
docker compose up --build
```

Compose поднимает три контейнера:

| Сервис   | Контейнер                   | Порт  |
|----------|-----------------------------|-------|
| PostgreSQL | `creative_db_container`   | 5432  |
| Backend  | `creative_backend_container` | 8000 |
| Frontend | `creative_frontend_container`| 3000 |

Backend дождётся готовности БД (healthcheck), создаст таблицы и заполнит демо-данными.

### 4. Открыть приложение

- Сайт: http://localhost:3000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Остановка

```bash
docker compose down
```

Данные PostgreSQL сохраняются в Docker-томе `postgres_data`. Чтобы удалить и их:

```bash
docker compose down -v
```

---

## Локальная разработка

### База данных

Запустите PostgreSQL (отдельно или только контейнер БД):

```bash
docker compose up db -d
```

### Backend

```bash
cd backend
python -m venv .venv

# Windows
.venv\Scripts\activate
# Linux / macOS
source .venv/bin/activate

pip install -r requirements.txt
```

Создайте файл `backend/.env` (Pydantic читает `.env` из рабочей директории backend):

```env
POSTGRES_USER=craft_user
POSTGRES_PASSWORD=change_me
POSTGRES_DB=craft_portal
POSTGRES_SERVER=localhost
POSTGRES_PORT=5432
SECRET_KEY=change_me_to_random_string
```

Запуск с hot-reload:

```bash
uvicorn app.main:app --reload --port 8000
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Приложение: http://localhost:3000  
Vite проксирует `/api` и `/media` на backend.

### Сборка frontend для production

```bash
cd frontend
npm run build
npm run preview
```

---

## Переменные окружения

Файл-образец: [`.env.example`](.env.example)

| Переменная           | Обязательна | Описание |
|----------------------|-------------|----------|
| `POSTGRES_USER`      | да          | Пользователь PostgreSQL |
| `POSTGRES_PASSWORD`  | да          | Пароль PostgreSQL |
| `POSTGRES_DB`        | да          | Имя базы данных |
| `POSTGRES_SERVER`    | да          | Хост БД (`db` в Docker, `localhost` локально) |
| `POSTGRES_PORT`      | да          | Порт PostgreSQL (обычно `5432`) |
| `SECRET_KEY`         | нет*        | Ключ подписи JWT. *В production обязательно задайте своё значение |

---

## Учётные записи по умолчанию

При первом запуске backend автоматически выполняет сидер ([`backend/app/models/seeder.py`](backend/app/models/seeder.py)).

**Пароль для всех демо-аккаунтов:** `password123`

| Роль        | Username         | Email              |
|-------------|------------------|--------------------|
| admin       | `admin`          | `admin@creative.me` |
| moderator   | `moderator_owl`  | `mod@creative.me`   |
| user        | `yarn_fairy`, `felt_artisan`, … | `*@craft.me` |

Сидер также создаёт 10 категорий, теги и 10 демо-публикаций.

> Сидер идемпотентен: повторный запуск не дублирует уже существующие записи.

---

## Роли и права доступа

| Роль        | Возможности |
|-------------|-------------|
| `user`      | Публикация работ, профиль, лайки, комментарии, редактирование/удаление своих постов |
| `moderator` | Всё выше + админка: модерация постов (скрытие/удаление), просмотр логов |
| `admin`     | Всё выше + управление пользователями, категориями, экспорт CSV |

JWT передаётся в заголовке:

```
Authorization: Bearer <access_token>
```

Токен выдаётся на 60 минут (`ACCESS_TOKEN_EXPIRE_MINUTES`).

---

## API

Базовый префикс: `/api`

### Авторизация (`/api/auth`)

| Метод | Путь | Описание |
|-------|------|----------|
| POST | `/register` | Регистрация (JSON) |
| POST | `/login` | Вход (form-data: `username`, `password`) |
| GET  | `/me` | Текущий пользователь |

> В поле `username` при логине можно передать email или username.

### Публикации (`/api/posts`)

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| GET  | `/` | — | Лента (query: `skip`, `limit`, `category_id`, `search`) |
| GET  | `/my` | ✓ | Мои публикации |
| POST | `/` | ✓ | Создание (multipart: `title`, `description`, `category_id`, `tags_json`, `file`) |
| GET  | `/{id}` | опц. | Детали публикации |
| PUT  | `/{id}` | ✓ | Редактирование (multipart) |
| DELETE | `/{id}` | ✓ | Удаление (автор или staff) |

### Комментарии (`/api/posts`)

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| GET  | `/{id}/comments/` | — | Список комментариев |
| POST | `/{id}/comments/` | ✓ | Добавить комментарий |
| DELETE | `/comments/{comment_id}` | ✓ | Удалить свой комментарий |

### Лайки (`/api/likes`)

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| POST   | `/{post_id}` | ✓ | Поставить лайк |
| DELETE | `/{post_id}` | ✓ | Убрать лайк |

### Профиль (`/api/profile`)

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| GET | `/` | ✓ | Профиль текущего пользователя |
| PUT | `/` | ✓ | Обновление (multipart: `username`, `email`, `bio`, `interest_ids`, `avatar`) |
| GET | `/comments` | ✓ | История комментариев |

### Категории (`/api/categories`)

| Метод | Путь | Auth | Описание |
|-------|------|------|----------|
| GET    | `/` | — | Список категорий |
| POST   | `/` | admin | Создание |
| PUT    | `/{id}` | admin | Переименование |
| DELETE | `/{id}` | admin | Удаление |

### Админка (`/api/admin`)

| Метод | Путь | Роль | Описание |
|-------|------|------|----------|
| GET   | `/users` | admin | Список пользователей |
| PATCH | `/users/{id}/role` | admin | Назначить роль |
| PATCH | `/users/{id}/toggle-status` | admin | Блокировка / разблокировка |
| GET   | `/users/export/csv` | admin | Экспорт пользователей |
| GET   | `/logs` | admin | Журнал действий |
| GET   | `/posts` | staff | Все публикации |
| PATCH | `/posts/{id}/toggle-hidden` | staff | Скрыть / показать |
| DELETE | `/posts/{id}` | staff | Удалить публикацию |

Полная интерактивная документация: http://localhost:8000/docs

---

## Маршруты frontend

| Путь | Доступ | Описание |
|------|--------|----------|
| `/` | все | Лента |
| `/posts/:id` | все | Страница публикации |
| `/posts/new` | auth | Создание публикации |
| `/posts/:id/edit` | auth | Редактирование |
| `/my-posts` | auth | Мои публикации |
| `/profile` | auth | Профиль |
| `/login`, `/register` | все | Авторизация |
| `/admin/*` | staff | Админ-панель |
| `/about`, `/help`, `/contacts`, `/events` | все | Информационные страницы |

---

## Медиафайлы

- Загрузка через `ImageService` ([`backend/app/core/image_service.py`](backend/app/core/image_service.py))
- Поддерживаемые форматы: `.jpg`, `.jpeg`, `.png`, `.webp`
- Максимальная сторона изображения: 1920 px (пропорции сохраняются)
- Файлы сохраняются в `backend/media/`
- URL в API: `/media/<uuid>.<ext>`
- Backend монтирует каталог как статику; в Docker он пробрасывается volume-ом

---

## Тестирование

Backend-тесты используют SQLite in-memory и не требуют PostgreSQL:

```bash
cd backend
pytest app/tests -q
```

Покрытие включает: регистрацию/логин, CRUD постов, профиль.

---

## Создание администратора вручную

Если нужен отдельный admin вне сидера:

```bash
cd backend
python -m app.create_admin
```

Скрипт создаст роли (если их нет) и пользователя:

- Email: `admin@example.com`
- Пароль: `admin123`

> Не используйте этот пароль в production.

---

## Устранение неполадок

### Backend не стартует: `ValidationError` для POSTGRES_*

Убедитесь, что `.env` существует и содержит все обязательные переменные.  
Для локального запуска файл должен лежать в `backend/.env`, для Docker — в корне проекта.

### Frontend не видит API

- Docker: проверьте, что backend-контейнер healthy (`docker compose ps`)
- Локально: backend должен слушать порт `8000`, frontend — `3000`

### Пустая лента после первого запуска

Дождитесь завершения сидера в логах backend (`База данных успешно заполнена!`).  
При ошибке сидера перезапустите backend или проверьте подключение к PostgreSQL.

### 401 после логина

Токен хранится в `localStorage`. Проверьте, что `SECRET_KEY` не менялся между перезапусками (иначе старые токены станут невалидными).

### Изображения не отображаются

- Убедитесь, что каталог `backend/media/` существует и доступен для записи
- Проверьте прокси `/media` (Vite или Nginx)

---