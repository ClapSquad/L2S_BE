from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.model.session import SessionModel

router = APIRouter(
    prefix="/admin",
    tags=["Admin"])


@router.post("/force-logout/{id}")
async def force_logout(id: int, db: Session = Depends(get_db)):
    sessions_deleted = db.query(SessionModel).filter(SessionModel.user_id == id).delete()

    if not sessions_deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active sessions found for this admin"
        )

    db.commit()
    return {"message": f"All sessions for admin {id} have been terminated."}
