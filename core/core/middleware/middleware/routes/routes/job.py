import logging

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from tasks.celery_tasks import process_image_task

router = APIRouter()
logger = logging.getLogger(__name__)


class JobRequest(BaseModel):
    image_url: str
    description_type: str = "detailed"


class JobResponse(BaseModel):
    task_id: str
    status: str


@router.post("/jobs", response_model=JobResponse)
async def create_job(job_request: JobRequest):
    """Создание задачи на описание изображения"""
    logger.info(
        f"Creating new job for image: {job_request.image_url}",
        extra={"job_type": "image_description"}
    )

    try:
        # Отправляем задачу в Celery
        task = process_image_task.delay(
            image_url=job_request.image_url,
            description_type=job_request.description_type
        )

        logger.info(
            f"Job created successfully with task_id: {task.id}",
            extra={"task_id": task.id}
        )

        return JobResponse(
            task_id=task.id,
            status="pending"
        )

    except Exception as e:
        logger.error(
            f"Failed to create job: {str(e)}",
            exc_info=True
        )
        raise HTTPException(status_code=500, detail="Failed to create job")


@router.get("/jobs/{task_id}")
async def get_job_status(task_id: str):
    """Получение статуса задачи"""
    logger.info(f"Checking status for task: {task_id}")

    from celery.result import AsyncResult
    from core.celery_app import celery_app

    task_result = AsyncResult(task_id, app=celery_app)

    if task_result.failed():
        logger.error(
            f"Task {task_id} failed: {str(task_result.result)}"
        )
        return {
            "task_id": task_id,
            "status": "failed",
            "error": str(task_result.result)
        }

    logger.info(
        f"Task {task_id} status: {task_result.status}"
    )

    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }
