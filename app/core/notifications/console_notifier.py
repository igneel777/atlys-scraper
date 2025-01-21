from logging import Logger

from app.core.models.notification import NotificationPayload
from app.core.notifications.base_notifier import BaseNotifier


class ConsoleNotifier(BaseNotifier):
    def __init__(self, logger: Logger):
        self.logger = logger

    def send_notification(self, notification_payload: NotificationPayload):
        self.logger.info(notification_payload.notification_message)
