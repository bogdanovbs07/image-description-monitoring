import logging

from core.celery_app import celery_app
from core.monitoring import monitor_task
from tasks.executor import executor

logger = logging.getLogger(__name__)


@celery_app.task(bind=True, name="process_image")
@monitor_task
def process_image_task(self, image_url: str, description_type: str = "detailed"):
    """Celery задача для обработки изображения"""
    logger.info(
        f"Starting image processing task",
        extra={
            "task_id": self.request.id,
            "image_url": image_url,
            "description_type": description_type
        }
    )

    try:
        # Обновляем статус задачи
        self.update_state(
            state="PROCESSING",
            meta={"progress": "Starting image description..."}
        )

        # Выполняем описание изображения
        logger.debug(f"Calling executor for image: {image_url}")
        result = executor.describe_image(image_url, description_type)

        logger.info(
            f"Task completed successfully",
            extra={"task_id": self.request.id}
        )

        return result

    except Exception as e:
        logger.error(
            f"Task failed: {str(e)}",
            exc_info=True,
            extra={"task_id": self.request.id}
        )
        self.update_state(
            state="FAILURE",
            meta={"error": str(e)}
        )
        raise
