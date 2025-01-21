from pydantic import BaseModel

class NotificationPayload(BaseModel):
    notification_message: str