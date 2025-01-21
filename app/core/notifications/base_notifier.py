from abc import ABC, abstractmethod

from app.core.models import NotificationPayload


class BaseNotifier(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def send_notification(self, notification_payload: NotificationPayload):
        pass
