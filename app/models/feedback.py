from app.models.base import BaseModel
from app.models.database import Database


class Feedback(BaseModel):

    @property
    def table(self):
        return "feedback"

    def __init__(
        self,
        user_id=None,
        subject=None,
        message=None,
        status="new"
    ):
        self.user_id = user_id
        self.subject = subject
        self.message = message
        self.status = status

    def save(self):
        db = Database()
        db.execute(
            """
            INSERT INTO feedback
            (user_id, subject, message, status)
            VALUES (%s,%s,%s,%s)
            """,
            (
                self.user_id,
                self.subject,
                self.message,
                self.status
            )
        )
        db.close()

    def get_user_feedback(self, user_id):
        db = Database()
        results = db.fetch_all(
            """
            SELECT *
            FROM feedback
            WHERE user_id=%s
            ORDER BY submitted_on DESC
            """,
            (user_id,)
        )
        db.close()
        return results

    def get_all_feedback(self):
        db = Database()
        results = db.fetch_all(
            """
            SELECT feedback.*, users.name AS user_name, users.email AS user_email
            FROM feedback
            JOIN users ON feedback.user_id = users.id
            ORDER BY feedback.submitted_on DESC
            """
        )
        db.close()
        return results

