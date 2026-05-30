import logging
import uuid

from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request


class RequestIDMiddleware(BaseHTTPMiddleware):
    """Middleware для добавления уникального ID к каждому запросу"""

    async def dispatch(self, request: Request, call_next):
        request_id = str(uuid.uuid4())
        request.state.request_id = request_id

        # Добавляем request_id в контекст логирования
        logger = logging.getLogger()
        logger_extra = {"request_id": request_id}

        # Логируем начало запроса
        logger.info(
            f"Incoming request: {request.method} {request.url.path}",
            extra=logger_extra
        )

        # Выполняем запрос
        response = await call_next(request)

        # Добавляем request_id в заголовки ответа
        response.headers["X-Request-ID"] = request_id

        # Логируем завершение запроса
        logger.info(
            f"Request completed: {response.status_code}",
            extra=logger_extra
        )

        return response
