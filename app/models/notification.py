from app.models.base import BaseModel
from app.models.database import Database


class Notification(BaseModel):

    @property
    def table(self):
        return "notifications"

    def __init__(
        self,
        user_id=None,
        report_id=None,
        message=None
    ):
        self.user_id = user_id
        self.report_id = report_id
        self.message = message

    def save(self):

        db = Database()

        db.execute(
            """
            INSERT INTO notifications
            (user_id, report_id, message)
            VALUES (%s,%s,%s)
            """,
            (
                self.user_id,
                self.report_id,
                self.message
            )
        )

        db.close()

    def get_user_notifications(self, user_id):

        db = Database()

        notifications = db.fetch_all(
            """
            SELECT *
            FROM notifications
            WHERE user_id=%s
            ORDER BY reported_on DESC
            """,
            (user_id,)
        )

        db.close()

        return notifications

    def mark_as_read(self, notification_id):

        db = Database()

        db.execute(
            """
            UPDATE notifications
            SET is_read=1
            WHERE id=%s
            """,
            (notification_id,)
        )

        db.close()