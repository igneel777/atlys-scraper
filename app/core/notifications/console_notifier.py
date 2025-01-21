from logging import Logger

from app.core.notifications.base_notifier import BaseNotifier
from app.core.models.notification import NotificationPayload



class ConsoleNotifier(BaseNotifier):

    def __init__(self, logger:Logger):
        self.logger = logger

    def send_notification(self, notification_payload:NotificationPayload):
        self.logger.info(notification_payload.notification_message)