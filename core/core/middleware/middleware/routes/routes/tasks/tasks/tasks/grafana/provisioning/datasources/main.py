from fastapi import FastAPI

from core.logging_config import setup_logging
from core.monitoring import setup_monitoring
from middleware.request_id import RequestIDMiddleware
from routes.job import router as job_router

# Настройка логирования
setup_logging()

# Создание приложения
app = FastAPI(title="Image Description Service")

# Добавление middleware
app.add_middleware(RequestIDMiddleware)

# Настройка мониторинга
setup_monitoring(app)

# Подключение роутов
app.include_router(job_router, prefix="/api/v1", tags=["jobs"])


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
