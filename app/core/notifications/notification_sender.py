from logging import Logger

from app.core.models.notification import NotificationPayload
from app.core.notifications.console_notifier import ConsoleNotifier


class NotificationSender:
    def __init__(self, logger: Logger):
        self.console_notifier: ConsoleNotifier = ConsoleNotifier(logger)

    def send_notification(self, notification_payload: NotificationPayload):
        self.console_notifier.send_notification(notification_payload)
