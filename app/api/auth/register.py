from fastapi import HTTPException, status, Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.model.user import UserModel
from app.db.dependency import get_db
from app.utility.security import hash_password
from app.api.router_base import router_auth as router


class RegisterModel(BaseModel):
    email: str
    username: str
    password: str


@router.post("/register")
async def register(data: RegisterModel, db: AsyncSession = Depends(get_db)):
    result = await db.execute(
        select(UserModel).where(UserModel.email == data.email)
    )
    existing_user = result.scalar_one_or_none()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="User already exists"
        )

    hashed_pw = hash_password(data.password)

    new_user = UserModel(
        email=data.email,
        username=data.username,
        password=hashed_pw,
        credit=0
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return {"message": "Successfully registered"}