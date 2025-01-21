import re
import time

import requests
from _io import TextIOWrapper
from bs4 import BeautifulSoup
from celery.utils.log import get_task_logger

from app.core import constants
from app.core.config import settings
from app.core.datastore import LocalFileStore, RedisAdapter
from app.core.dependencies.service_dependencies import get_product_service
from app.core.models import NotificationPayload, ProductInDB
from app.task_queue.celery_app import send_notification

logger = get_task_logger(__name__)


class Scraper:
    headers = constants.HEADERS
    max_retries = constants.SCRAPE_RETRIES
    base_url = constants.SCRAPE_URL

    def __init__(self, proxy: str | None = None):
        self.proxies = {"http": proxy, "https": proxy} if proxy else None
        self.file_store = LocalFileStore()
        self.cache_store = RedisAdapter()

    def _get_page_html(self, page_num: int) -> str:
        url = self.base_url + f"{page_num}/"
        for attempt in range(self.max_retries):
            try:
                response = requests.get(
                    url,
                    headers=self.headers,
                    proxies=self.proxies,
                    timeout=30,
                )
                response.raise_for_status()
                return response.text
            except Exception as ex:
                if attempt == self.max_retries - 1:  # Last attempt
                    logger.info(f"Scraping for page: {page_num} failed.")
                    logger.info(f"Tries left = {self.max_retries - attempt - 1}.")
                    logger.info(
                        f"Retrying after {constants.SCRAPE_PAGE_RETRY_DELAY} seconds."
                    )
                    err_message = f"Scraping for page: {page_num} failed. Tries left = {self.max_retries - attempt - 1}. Retrying after {constants.SCRAPE_PAGE_RETRY_DELAY} seconds"

                else:
                    err_message = f"Scraping for page: {page_num} failed. No retries."
                    logger.error(err_message)
                    raise ex

                time.sleep(constants.SCRAPE_PAGE_RETRY_DELAY)
                send_notification.delay(
                    NotificationPayload(notification_message=err_message)
                )
        return ""

    def _save_image_in_filestore(self, source_url: str, image_key: str) -> str:
        return self.file_store.save_file_from_url(source_url, image_key)

    def _get_price_from_str(self, price_str: str) -> float:
        match = re.match(r"₹([\d.]+)", price_str)
        if match:
            amount = float(match.group(1))
        else:
            amount = 0.0
        return amount

    def _get_product_list(self, html_page: str) -> list[ProductInDB]:
        soup = BeautifulSoup(html_page, "html.parser")
        products_html = soup.find_all("div", class_="product-inner")

        product_list = []
        for product_html in products_html:
            try:
                price_str = (
                    product_html.find("span", class_="price").find("bdi").get_text()
                )
                price = self._get_price_from_str(price_str)
                product_name = (
                    product_html.find("h2", class_="woo-loop-product__title")
                    .get_text()
                    .strip(".")
                )
                image_url = product_html.find("img").get("data-lazy-src")
                image_key = f"{product_name}.jpg"
                image_key = self._save_image_in_filestore(image_url, image_key)

                cached_value = self.cache_store.get_values(product_name)
                if not cached_value or cached_value != price:
                    self.cache_store.set_values(product_name, price, {"days": 1})
                    product_list.append(
                        ProductInDB(
                            price=price,
                            product_name=product_name,
                            image_url=image_url,
                            image_key=image_key,
                        )
                    )
            except Exception as ex:
                logger.error(ex)
                pass

        return product_list

    def get_products_from_page(self, page_num: int):
        html_text = self._get_page_html(page_num)
        product_list = []
        if html_text:
            product_list = self._get_product_list(html_text)
        return product_list


def run_scrape_task(page_num: int, proxy: str | None, db_connection: TextIOWrapper):
    product_service = get_product_service(db_connection)
    scraper = Scraper(proxy)

    products_fetched = scraper.get_products_from_page(page_num)
    product_service.insert_in_db_bulk(products_fetched)
    successfull_message = (
        f"Fetched {len(products_fetched)} product info from page {page_num}."
    )
    send_notification(NotificationPayload(notification_message=successfull_message))
