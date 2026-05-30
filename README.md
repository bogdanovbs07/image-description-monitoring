# Image Description Monitoring Service

Сервис для описания изображений с системой мониторинга и логирования.

## Стек технологий
- FastAPI (API)
- Celery (фоновые задачи)
- PostgreSQL (база данных)
- Redis (кэш и брокер сообщений)
- Prometheus (сбор метрик)
- Grafana (визуализация)
- Flower (мониторинг Celery)
- Docker Compose (контейнеризация)

## Запуск проекта

```bash
docker-compose up -d

Сервисы
API: http://localhost:8000

Flower: http://localhost:5555

Prometheus: http://localhost:9090

Grafana: http://localhost:3000 (admin/admin)


4. Нажмите **"Commit changes..."**
5. В появившемся окне нажмите **"Commit changes"** (зелёная кнопка)

#### 2.2 Создаём папку `core/` и файлы в ней

**Файл `core/__init__.py`:**
1. Нажмите **"Add file"** → **"Create new file"**
2. В поле имени введите: `core/__init__.py`
3. Содержимое оставьте пустым
4. Нажмите **"Commit changes..."** → **"Commit changes"**

**Файл `core/logging_config.py`:**
1. Нажмите **"Add file"** → **"Create new file"**
2. В поле имени введите: `core/logging_config.py`
3. Вставьте следующий код:
```python
import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


def setup_logging():
    """Настройка логирования для всего приложения"""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)

    # Форматтер с request_id
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - [%(request_id)s] - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    # Обработчик для файла с ротацией
    file_handler = RotatingFileHandler(
        log_dir / "app.log",
        maxBytes=10485760,  # 10MB
        backupCount=5
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.INFO)

    # Обработчик для консоли
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    console_handler.setLevel(logging.DEBUG)

    # Настройка корневого логгера
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)

    return root_logger
