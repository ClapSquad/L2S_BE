from pathlib import Path
from fastapi import APIRouter, Request, HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.model.session import SessionModel
from app.model.video import VideoModel
from app.model.user import UserModel
from datetime import datetime
from app.utility.youtube import download_youtube_video

router = APIRouter(
    prefix="/video",
    tags=["Video"]
)

UPLOAD_DIR = Path(__file__).resolve().parents[3] / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)


class YouTubeUploadRequest(BaseModel):
    youtube_id: str


@router.post("/upload/youtube")
async def upload_youtube_video(request: Request, data: YouTubeUploadRequest, db: Session = Depends(get_db)):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Login required"
        )

    session = db.query(SessionModel).filter(SessionModel.session_token == session_token).first()
    if not session or (session.expires_at and session.expires_at < datetime.utcnow()):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Session expired or invalid"
        )

    user = db.query(UserModel).filter(UserModel.id == session.user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    try:
        file_path, video_title = download_youtube_video(data.youtube_id, UPLOAD_DIR)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred while downloading the video"
        )

    video = VideoModel(
        user_id=user.id,
        file_path=str(file_path),
        youtube_id=data.youtube_id
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    return {
        "message": f"YouTube video '{video_title}' downloaded successfully!",
        "video_id": video.id,
    }