from fastapi import HTTPException, status, Depends
from sqlalchemy.orm import Session
from app.db.dependency import get_db
from app.model.session import SessionModel
from app.api.router_base import router_admin as router


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
