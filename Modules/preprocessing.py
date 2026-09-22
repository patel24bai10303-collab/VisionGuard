from pathlib import Path
import shutil

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png"}
VIDEO_EXTENSIONS = {".mp4", ".avi", ".mov", ".mkv"}

def validate_media(filename: str):
    ext = Path(filename).suffix.lower()
    if ext in IMAGE_EXTENSIONS:
        return True, "Valid image", "image"
    if ext in VIDEO_EXTENSIONS:
        return True, "Valid video", "video"
    return False, "Unsupported file type. Use JPG, JPEG, PNG, MP4, AVI, MOV or MKV.", None

def save_uploaded_file(uploaded_file, directory: Path) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    destination = directory / Path(uploaded_file.name).name
    with open(destination, "wb") as output:
        shutil.copyfileobj(uploaded_file, output)
    return destination

def resize_keep_aspect(image, max_width: int):
    import cv2
    h, w = image.shape[:2]
    if w <= max_width:
        return image
    scale = max_width / w
    return cv2.resize(image, (max_width, int(h * scale)), interpolation=cv2.INTER_AREA)
