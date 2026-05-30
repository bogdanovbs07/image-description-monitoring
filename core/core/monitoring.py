import time
from functools import wraps

from prometheus_client import Counter, Histogram, generate_latest, REGISTRY
from prometheus_fastapi_instrumentator import Instrumentator

# Метрики
REQUEST_COUNT = Counter(
    "http_requests_total",
    "Total HTTP requests",
    ["method", "endpoint", "status"]
)

REQUEST_LATENCY = Histogram(
    "http_request_duration_seconds",
    "HTTP request latency",
    ["method", "endpoint"]
)

TASK_COUNT = Counter(
    "celery_tasks_total",
    "Total Celery tasks",
    ["task_name", "status"]
)

TASK_DURATION = Histogram(
    "celery_task_duration_seconds",
    "Celery task duration",
    ["task_name"]
)


def monitor_task(func):
    """Декоратор для мониторинга Celery задач"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        task_name = func.__name__
        start_time = time.time()

        try:
            result = func(*args, **kwargs)
            TASK_COUNT.labels(task_name=task_name, status="success").inc()
            return result
        except Exception as e:
            TASK_COUNT.labels(task_name=task_name, status="error").inc()
            raise e
        finally:
            duration = time.time() - start_time
            TASK_DURATION.labels(task_name=task_name).observe(duration)

    return wrapper


def setup_monitoring(app):
    """Настройка мониторинга для FastAPI приложения"""
    instrumentator = Instrumentator()
    instrumentator.instrument(app).expose(app)

    @app.get("/metrics")
    async def metrics():
        return generate_latest(REGISTRY)
