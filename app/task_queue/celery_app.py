import logging
from contextlib import contextmanager
from logging import Logger

from celery import Celery
from celery.signals import (after_setup_logger, after_setup_task_logger,
                            task_prerun)

from app.core.config import settings
from app.core.datastore import LocalDatabase
from app.core.models.notification import NotificationPayload

celery_app = Celery(broker=settings.REDIS_URL.unicode_string())

celery_app.conf.update(
    worker_concurrency=1,  # Only one task at a time
    worker_prefetch_multiplier=1,  # Only one task picked up at a time
    task_track_started=True,
    task_acks_late=True,
)


def setup_loggers(logger: Logger, *args, **kwargs):
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # add filehandler
    file_handler = logging.FileHandler("celery_app.log")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # stream_handler = logging.StreamHandler()
    # stream_handler.setFormatter(formatter)
    # stream_handler.setLevel(logging.DEBUG)

    # logger.addHandler(stream_handler)
    logger.addHandler(file_handler)


@after_setup_logger.connect
def setup_celery_logger(logger: Logger, *args, **kwargs):
    setup_loggers(logger, *args, **kwargs)


@after_setup_task_logger.connect
def setup_task_logger(logger: Logger, *args, **kwargs):
    setup_loggers(logger, *args, **kwargs)


@task_prerun.connect
def reset_connection(**kwargs):
    # This will run before every task
    local_db = LocalDatabase()
    local_db.refresh_connection()


@contextmanager
def _get_dependencies():
    local_db = LocalDatabase()
    local_db.refresh_connection()

    db_connection = local_db.get_connection()

    dependencies = {}
    dependencies["db_connection"] = db_connection

    yield dependencies

    db_connection.close()


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 0})
def run_scraping(page_num: int, proxy: str):
    from .tasks.run_scrape_task import run_scrape_task

    with _get_dependencies() as dependencies:
        run_scrape_task(page_num, proxy, **dependencies)


@celery_app.task(autoretry_for=(Exception,), retry_kwargs={"max_retries": 3})
def send_notification(notification_payload: NotificationPayload):
    from .tasks.notification_send import notification_send

    notification_send(notification_payload)
