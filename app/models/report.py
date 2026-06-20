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

    def search_user_reports(self, user_id, search_term):

        db = Database()

        like_term = f"%{search_term}%"

        reports = db.fetch_all(
            """
            SELECT *
            FROM reports
            WHERE user_id=%s
            AND (waste_type LIKE %s OR location LIKE %s OR description LIKE %s)
            ORDER BY reported_on DESC
            """,
            (user_id, like_term, like_term, like_term)
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

    def delete_by_id(self, report_id):
        db = Database()
        # Delete notifications linked to this report first
        db.execute("DELETE FROM notifications WHERE report_id=%s", (report_id,))
        # Then delete the report
        db.execute("DELETE FROM reports WHERE id=%s", (report_id,))
        db.close()

    def _save_image(self, image_file):
        import os
        from flask import current_app
        if not image_file or not image_file.filename:
            return None
        upload_folder = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        filename = image_file.filename
        filepath = os.path.join(upload_folder, filename)
        image_file.save(filepath)
        return filename

    def update_report(self, report_id, location, waste_type, description, image_file):
        image_path = self._save_image(image_file)
        db = Database()
        if image_path:
            db.execute(
                """
                UPDATE reports
                SET location=%s, waste_type=%s, description=%s, image_path=%s
                WHERE id=%s
                """,
                (location, waste_type, description, image_path, report_id)
            )
        else:
            db.execute(
                """
                UPDATE reports
                SET location=%s, waste_type=%s, description=%s
                WHERE id=%s
                """,
                (location, waste_type, description, report_id)
            )
        db.close()