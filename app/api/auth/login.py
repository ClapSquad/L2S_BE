from fastapi import APIRouter, Request, Response, HTTPException, status, Depends
from pydantic import BaseModel
from app.model.user import UserModel
from sqlalchemy.orm import Session
from app.db.dependency import get_db

router = APIRouter(
    prefix="/auth",
    tags=["Auth"])


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/login")
async def login(
        request: Request,
        response: Response,
        data: LoginRequest,
        db: Session = Depends(get_db)
):
    user = db.query(UserModel).filter(UserModel.email == data.email).first()
    if not user or user.password != data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Id or password is not correct"
        )

    request.session["user_id"] = user.id

    return {
        "message": "Successfully logged in"
    }
