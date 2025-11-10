from fastapi import APIRouter, HTTPException, status, Depends
from pydantic import BaseModel
from app.model.user import UserModel
from sqlalchemy.orm import Session
from app.db.dependency import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"])


class RegisterModel(BaseModel):
    email: str
    username: str
    password: str


@router.post("/register")
async def register(data: RegisterModel, db: Session = Depends(get_db)):
    existing_user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    new_user = UserModel(
        email=data.email,
        username=data.username,
        password=data.password,
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": "Successfully registered"}
