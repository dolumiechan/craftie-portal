# Шаг 1: Используем официальный легковесный образ Python

# Шаг 2: Установка системных утилит и библиотек для сборки бинарных зависимостей (например, psycopg2 для PostgreSQL)
RUN apt-get update && apt-get install -y \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Шаг 3: Настройка рабочей директории внутри контейнера
WORKDIR /app

# Шаг 4: Кэширование слоя зависимостей. Копируем requirements отдельно,
# чтобы не пересобирать пакеты при изменении кода приложения.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Шаг 5: Копирование исходного кода бэкенда в контейнер
COPY . .

# Шаг 6: Открытие порта для сетевого взаимодействия внутри Docker-сети
EXPOSE 8000

# Шаг 7: Команда запуска ASGI-сервера Uvicorn.
# --proxy-headers сообщает Uvicorn, что он работает за прокси-сервером (Docker/Nginx)
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]