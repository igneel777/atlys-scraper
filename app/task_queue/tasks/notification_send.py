from celery.utils.log import get_task_logger

from app.core.models.notification import NotificationPayload
from app.core.notifications.notification_sender import NotificationSender

logger = get_task_logger(__name__)

def notification_send(notification_payload:NotificationPayload):
    notification_sender = NotificationSender(logger)
    notification_sender.send_notification(notification_payload)