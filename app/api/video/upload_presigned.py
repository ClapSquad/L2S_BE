import uuid
from pathlib import Path
from fastapi import  Request, HTTPException, Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.model.session import SessionModel
from app.model.user import UserModel
from datetime import datetime, UTC
from app.config.environments import SUPABASE_PROJECT_URL, SUPABASE_SERVICE_KEY
from app.api.router_base import router_video as router
import requests


@router.get("/upload/presign")
async def upload_presigned(
        request: Request,
        filename: str,
        content_type: str,
        db: Session = Depends(get_db)
):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(status_code=401, detail="Login required")

    session = db.query(SessionModel).filter(SessionModel.session_token == session_token).first()
    if not session or (session.expires_at and session.expires_at < datetime.now(UTC)):
        raise HTTPException(status_code=401, detail="Session expired or invalid")

    user = db.query(UserModel).filter(UserModel.id == session.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if user.credit < 1:
        raise HTTPException(status_code=402, detail="Insufficient credit")

    file_extension = Path(filename).suffix
    video_uuid = str(uuid.uuid4())
    unique_filename = f"{video_uuid}{file_extension}"

    response = requests.post(
        f"{SUPABASE_PROJECT_URL}/storage/v1/object/upload/sign/videos/{unique_filename}",
        headers={
            "Authorization": f"Bearer {SUPABASE_SERVICE_KEY}",
            "Content-Type": "application/json"
        },
        json={"expiresIn": 1800}
    )

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Failed to generate presigned URL")

    data = response.json()

    return {
        "presigned_url": f"{SUPABASE_PROJECT_URL}/storage/v1{data['url']}",
        "video_uuid": video_uuid,
        "filename": unique_filename,
        "user_id": user.id
    }