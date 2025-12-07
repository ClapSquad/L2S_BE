from fastapi import HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete
from app.db.dependency import get_db
from app.model.session import SessionModel
from app.api.router_base import router_admin as router


@router.post("/force-logout/{id}")
async def force_logout(id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(delete(SessionModel).where(SessionModel.user_id == id))

    if result.rowcount == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No active sessions found for this user"
        )

    await db.commit()
    return {"message": f"All sessions for user {id} have been terminated."}
