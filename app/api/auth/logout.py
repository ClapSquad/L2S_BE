from fastapi import Request, Response, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.db.dependency import get_db
from app.model.session import SessionModel
from app.config.environments import ENVIRONMENT
from app.api.router_base import router_auth as router


COOKIE_SECURE = False
COOKIE_SAMESITE = "lax"
if ENVIRONMENT == "production":
    COOKIE_SECURE = True
    COOKIE_SAMESITE = "none"


@router.post("/logout")
async def logout(request: Request, response: Response, db: AsyncSession = Depends(get_db)):
    session_token = request.cookies.get("session_token")
    if not session_token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not logged in"
        )

    await db.execute(
        delete(SessionModel).where(SessionModel.session_token == session_token)
    )
    await db.commit()

    response.delete_cookie(
        "session_token",
        httponly=True,
        secure=COOKIE_SECURE,
        samesite=COOKIE_SAMESITE
    )

    return {"message": "Successfully logged out"}