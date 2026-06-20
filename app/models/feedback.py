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

    

    