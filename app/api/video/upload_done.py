from fastapi import Request, HTTPException, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.model.session import SessionModel
from app.model.video import VideoModel
from app.model.user import UserModel
from datetime import datetime, UTC
from app.config.environments import SUPABASE_PROJECT_URL, RUNPOD_URL, RUNPOD_API_KEY
from app.api.router_base import router_video as router
import requests


class UploadDoneRequest(BaseModel):
    video_uuid: str
    original_filename: str
    filename: str


@router.post("/upload/done")
async def upload_done(
        request: Request,
        body: UploadDoneRequest,
        db: Session = Depends(get_db)
):
    # 인증 체크 (동일)
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Login required")

    session = db.query(SessionModel).filter(SessionModel.session_token == session_token).first()
    if not session or (session.expires_at and session.expires_at < datetime.now(UTC)):
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    user = db.query(UserModel).filter(UserModel.id == session.user_id).first()
    if not user or user.credit < 1:
        raise HTTPException(status_code=402, detail="Insufficient credit")

    file_url = f"{SUPABASE_PROJECT_URL}/storage/v1/object/public/videos/{body.filename}"

    # 썸네일 생성 요청
    requests.post(
        url=f"{RUNPOD_URL}/run",
        headers={
            "Content-Type": "application/json",
            "Authorization": f"Bearer {RUNPOD_API_KEY}"
        },
        json={
            "input": {
                "job_id": body.video_uuid,
                "task": "generate_thumbnail",
                "video_url": file_url
            }
        }
    )

    thumbnail_url = file_url.replace("/videos/", "/thumbnails/")
    if thumbnail_url.endswith(".mp4"):
        thumbnail_url = thumbnail_url[:-4] + ".jpg"

    video = VideoModel(
        user_id=user.id,
        file_path=file_url,
        name=body.original_filename,
        thumbnail_path=thumbnail_url,
        youtube_id=None
    )
    db.add(video)
    db.commit()
    db.refresh(video)

    user.credit -= 1
    db.commit()

    return {
        "message": "Upload completed",
        "video_id": video.id,
        "video_url": file_url,
        "thumbnail_url": thumbnail_url
    }