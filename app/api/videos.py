from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from pytube import YouTube
import os
from app.model.video import VideoModel
from app.db.dependency import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/videos",
    tags=["Videos"]
)

class YouTubeRequest(BaseModel):
    url: str
    title: str

@router.post("/download-youtube")
def download_youtube(request: YouTubeRequest, db: Session = Depends(get_db)):
    try:
        yt = YouTube(request.url)
        stream = yt.streams.get_highest_resolution()
        os.makedirs("temp_videos", exist_ok=True)
        file_path = os.path.join("temp_videos", f"{request.title}.mp4")
        stream.download(output_path="temp_videos", filename=f"{request.title}.mp4")

        video = VideoModel(title=request.title, youtube_url=request.url, file_path=file_path)
        db.add(video)
        db.commit()
        db.refresh(video)

        return {"message": "Video downloaded", "video_id": video.id, "file_path": file_path}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
