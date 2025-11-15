from pathlib import Path
from fastapi import APIRouter, UploadFile, File
import os, shutil

router = APIRouter(
    prefix="/video",
    tags=["Video"])


UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = os.path.join(UPLOAD_DIR, file.filename)

    # Use shutil.copyfileobj for large files
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"message": f"File '{file.filename}' uploaded successfully!"}
