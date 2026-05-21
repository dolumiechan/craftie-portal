<<<<<<< HEAD
import os
import uuid
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

class ImageService:
    def __init__(self, upload_dir: str = "media"):
        self.upload_dir = upload_dir
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def validate_and_save_image(self, file: UploadFile) -> str:
        """
        Проверяет, что файл является корректным изображением, 
        генерирует уникальное имя и сохраняет его на диск.
        Возвращает путь к файлу для сохранения в БД.
        """
        valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in valid_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Недопустимый формат файла. Разрешены только: {', '.join(valid_extensions)}"
            )

        try:
            file_content = file.file.read()
            image = Image.open(io.BytesIO(file_content))
            image.verify()
            
            file.file.seek(0)
        except Exception:
            raise HTTPException(
                status_code=400, 
                detail="Файл поврежден или не является валидным изображением."
            )

        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        return f"media/{unique_filename}"

=======
import os
import uuid
from fastapi import UploadFile, HTTPException
from PIL import Image
import io

class ImageService:
    def __init__(self, upload_dir: str = "media"):
        self.upload_dir = upload_dir
        if not os.path.exists(self.upload_dir):
            os.makedirs(self.upload_dir)

    def validate_and_save_image(self, file: UploadFile) -> str:
        """
        Проверяет, что файл является корректным изображением, 
        генерирует уникальное имя и сохраняет его на диск.
        Возвращает путь к файлу для сохранения в БД.
        """
        valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
        file_ext = os.path.splitext(file.filename)[1].lower()
        if file_ext not in valid_extensions:
            raise HTTPException(
                status_code=400, 
                detail=f"Недопустимый формат файла. Разрешены только: {', '.join(valid_extensions)}"
            )

        try:
            file_content = file.file.read()
            image = Image.open(io.BytesIO(file_content))
            image.verify()
            
            file.file.seek(0)
        except Exception:
            raise HTTPException(
                status_code=400, 
                detail="Файл поврежден или не является валидным изображением."
            )

        unique_filename = f"{uuid.uuid4()}{file_ext}"
        file_path = os.path.join(self.upload_dir, unique_filename)

        with open(file_path, "wb") as buffer:
            buffer.write(file_content)

        return f"media/{unique_filename}"

>>>>>>> 8d6cb81 (Add posts filtering/search with pagination and implement admin endpoints)
image_service = ImageService()