from app.models.base import BaseModel
from app.models.database import Database

class Report(BaseModel):

    @property
    def table(self):
        return "reports"

    def __init__(
        self,
        user_id=None,
        waste_type =None,
        description=None,
        location=None,
        image_path=None,
        status="pending"
    ):
        self.user_id = user_id
        self.waste_type  = waste_type 
        self.description = description
        self.location = location
        self.image_path = image_path
        self.status = status

    def save(self):
        db = Database()

        db.execute(
            """
            INSERT INTO reports
            (user_id, waste_type , description, location, image_path, status)
            VALUES (%s,%s,%s,%s,%s,%s)
            """,
            (
                self.user_id,
                self.waste_type ,
                self.description,
                self.location,
                self.image_path,
                self.status
            )
        )

        db.close()

    def get_user_reports(self, user_id):

        db = Database()

        reports = db.fetch_all(
            """
            SELECT *
            FROM reports
            WHERE user_id=%s
            ORDER BY reported_on  DESC
            """,
            (user_id,)
        )

        db.close()

        return reports
    
    def get_reports_by_status(self, user_id, status):

        db = Database()

        reports = db.fetch_all(
            """
            SELECT *
            FROM reports
            WHERE user_id=%s
            AND status=%s
            """,
            (user_id, status)
        )

        db.close()

        return reports
    
    def update_status(self, report_id, status):

        db = Database()

        db.execute(
            """
            UPDATE reports
            SET status=%s
            WHERE id=%s
            """,
            (status, report_id)
        )
    
        db.close()