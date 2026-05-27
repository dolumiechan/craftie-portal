import os
import uuid
import io

from fastapi import UploadFile, HTTPException
from PIL import Image, ImageOps

UPLOAD_DIR = "media"

class ImageService:
    def __init__(self, upload_dir: str = UPLOAD_DIR, max_side: int = 1920):
        self.upload_dir = upload_dir
        self.max_side = max_side
        os.makedirs(self.upload_dir, exist_ok=True)

    def validate_and_save_image(self, file: UploadFile) -> str:
        valid_extensions = [".jpg", ".jpeg", ".png", ".webp"]
        file_ext = os.path.splitext(file.filename or "")[1].lower()
        if file_ext not in valid_extensions:
            raise HTTPException(
                status_code=400,
                detail=f"Недопустимый формат. Разрешены: {', '.join(valid_extensions)}",
            )

        try:
            file_content = file.file.read()
            image = Image.open(io.BytesIO(file_content))
            image.verify()
            image = Image.open(io.BytesIO(file_content))

            w, h = image.size
            if max(w, h) > self.max_side:
                image = ImageOps.contain(image, (self.max_side, self.max_side))

            unique_filename = f"{uuid.uuid4()}{file_ext}"
            file_path = os.path.join(self.upload_dir, unique_filename)
            image.save(file_path, optimize=True)
            return f"/media/{unique_filename}"
        except HTTPException:
            raise
        except Exception:
            raise HTTPException(
                status_code=400,
                detail="Файл повреждён или не является изображением.",
            )


image_service = ImageService()
