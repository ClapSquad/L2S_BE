from fastapi import APIRouter, Request, HTTPException, status, Depends
from app.model.user import UserModel
from sqlalchemy.orm import Session
from app.db.dependency import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"])


@router.get("/me")
async def get_current_user(request: Request, db: Session = Depends(get_db)):
    user_id = request.session.get("user_id")
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Require login"
        )

    user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )

    return {"user": {"email": user.email, "username": user.username}}
