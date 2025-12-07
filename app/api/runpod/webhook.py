from fastapi import Request, HTTPException, status, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.dependency import get_db
from app.model.job import JobModel, JobStatus
from app.model.user import UserModel
from datetime import datetime, UTC
from app.api.router_base import router_runpod as router


@router.post("/webhook/{job_id}")
async def runpod_webhook(job_id: str, request: Request, db: AsyncSession = Depends(get_db)):
    try:
        payload = await request.json()

        webhook_status = payload.get("status")
        result_url = payload.get("result_url")
        error = payload.get("error")

        if not job_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Missing job_id in webhook payload"
            )

        result = await db.execute(
            select(JobModel).where(JobModel.id == int(job_id))
        )
        job = result.scalar_one_or_none()

        if not job:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Job {job_id} not found"
            )

        if webhook_status == "completed":
            job.status = JobStatus.COMPLETED
            job.result_url = result_url
            job.completed_at = datetime.now(UTC)
        elif webhook_status == "failed":
            job.status = JobStatus.FAILED
            job.error_message = error
            job.completed_at = datetime.now(UTC)

            result = await db.execute(
                select(UserModel).where(UserModel.id == job.user_id)
            )
            user = result.scalar_one_or_none()
            if user:
                user.credit += 1
        else:
            job.error_message = f"Unknown status from webhook: {webhook_status}"

        await db.commit()

        return {
            "message": "Webhook received successfully",
            "job_id": job_id,
            "status": job.status
        }

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process webhook: {str(e)}"
        )