from fastapi import APIRouter, Body, status

from app.logger import logger
from app.task_queue.celery_app import run_scraping

router = APIRouter()


@router.post("/scrape-products", status_code=status.HTTP_202_ACCEPTED)
def enqueue_scraping_job(
    skip: int = Body(0),
    limit: int = Body(5),
    proxy_url: str = Body(None),
):
    page_list = list(range(skip + 1, skip + limit + 1))
    for page_num in page_list:
        run_scraping.delay(page_num, proxy_url)
