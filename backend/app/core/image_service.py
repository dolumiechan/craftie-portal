import os
import uuid
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

class ImageService:
    """
    Выделенный сервис обработки и валидации медиаконтента.
    
    Изолирует логику работы с файловой системой и графической библиотекой Pillow.
    Обеспечивает централизованную проверку безопасности загружаемых файлов перед их сохранением.
    """
    def __init__(self, upload_dir: str = "media"):
        # Инициализируем и проверяем наличие целевой директории для статики
        self.upload_dir = upload_dir
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def validate_and_save_image(self, file: UploadFile) -> str:
        """
        Комплексная валидация и безопасное сохранение графического файла.
        
        Алгоритм работы:
        1. Проверка допустимых расширений (белый список форматов).
        2. Сигнатурный анализ файла с помощью Pillow (метод verify) для защиты 
           от маскировки вредоносного исполняемого кода под расширение картинки.
        3. Генерация криптографически стойкого уникального имени (UUID) для предотвращения коллизий.
        4. Запись бинарного потока в media-папку сервера.
        
        :param file: Объект загруженного файла FastAPI (UploadFile).
        :return: Относительный веб-путь к сохраненному файлу для записи в БД.
        """
        # 1. ПЕРВИЧНЫЙ ФИЛЬТР: Проверка расширения по белому списку
        valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in valid_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Недопустимый формат файла. Разрешены только: {', '.join(valid_extensions)}"
            )

        try:
            # Читаем бинарное содержимое файла в оперативную память (буфер)
            file_content = file.file.read()
            
            # 2. ГЛУБОКАЯ ВАЛИДАЦИЯ:
            # Открываем байты как объект изображения и проверяем целостность заголовков (структуру файла)
            image = Image.open(io.BytesIO(file_content))
            image.verify()  # Выбросит исключение, если файл битый или это замаскированный скрипт
            
            # Сбрасываем указатель чтения потока обратно на 0-й байт. Это необходимо для страховки,
            # чтобы при повторном обращении к объекту файла в коде его можно было прочитать заново.
            file.file.seek(0)
        except Exception:
            raise HTTPException(
                status_code=400, 
                detail="Файл поврежден, изменен или не является валидным изображением."
            )

        # 3. ЗАЩИТА ОТ КОНФЛИКТОВ И СОХРАНЕНИЕ НА ДИСК
        # Генерируем случайный шестнадцатеричный идентификатор, чтобы имена файлов никогда не пересекались
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        # Открываем файл на сервере в режиме записи байт (wb) и сбрасываем буфер из памяти на диск
        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        # Возвращаем путь, который запишется в базу данных и будет использоваться фронтендом
        return f"media/{unique_filename}"

# Создаем синглтон для переиспользования во всех роутерах бэкенда
image_service = ImageService()