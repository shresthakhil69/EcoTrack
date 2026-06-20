from .base import BaseModel
from datetime import datetime
import os
from flask import current_app


class Report(BaseModel):
    """Report Model - Handles all report database operations"""

    @property
    def table(self):
        return "reports"

    def _save_image(self, image_file):
        """
        Save image file to uploads folder.
        
        Args:
            image_file: Flask FileStorage object
        
        Returns:
            str: Path to saved image or None if no image
        """
        if not image_file or not image_file.filename:
            return None
        
        # Create uploads folder if it doesn't exist
        upload_folder = os.path.join(current_app.root_path, "static", "uploads")
        os.makedirs(upload_folder, exist_ok=True)
        
        # Save the file
        filename = image_file.filename
        filepath = os.path.join(upload_folder, filename)
        image_file.save(filepath)
        
        # Return relative path for database
        return f"uploads/{filename}"
    
    def create(self, user_id, location, waste_type, description, image_file):
        """
        Create a new report with image file.
        
        Args:
            user_id (int): User who submitted the report
            location (str): Report location
            waste_type (str): Type of waste
            description (str): Report description
            image_file: Flask FileStorage object
        
        Returns:
            int: ID of created report or None if failed
        """
        from .database import Database
        
        # Save image to filesystem
        image_path = self._save_image(image_file)
        
        # Insert report into database
        db = Database()
        query = f"""
            INSERT INTO {self.table} (user_id, location, waste_type, description, image_path, status, reported_on)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        
        report_id = db.execute(query, (
            user_id,
            location,
            waste_type,
            description,
            image_path,
            "pending",
            datetime.utcnow()
        ))
        
        db.close()
        return report_id

    def get_user_reports(self, user_id):
        """
        Get all reports submitted by a specific user.
        
        Args:
            user_id (int): ID of the user
        
        Returns:
            list: List of reports or empty list if none found
        """
        from .database import Database
        
        db = Database()
        query = f"""
            SELECT id, waste_type, location, description, image_path, status, reported_on
            FROM {self.table}
            WHERE user_id = %s
            ORDER BY reported_on DESC
        """
        results = db.fetch_all(query, (user_id,))
        db.close()
        return results

    def get_all_reports(self):
        """
        Get all reports from all users with user information.
        
        Returns:
            list: List of all reports ordered by most recent first
        """
        from .database import Database
        
        db = Database()
        query = f"""
            SELECT r.id, r.waste_type, r.location, r.description, r.image_path, r.status, r.reported_on, u.name as user_name
            FROM {self.table} r
            JOIN users u ON r.user_id = u.id
            ORDER BY r.reported_on DESC
        """
        results = db.fetch_all(query)
        db.close()
        return results

    def update_status(self, report_id, status):
        """
        Update the status of a report.
        
        Args:
            report_id (int): ID of the report
            status (str): New status ('pending', 'in_progress', 'resolved')
        
        Returns:
            bool: True if updated successfully, False otherwise
        """
        from .database import Database
        
        db = Database()
        query = f"UPDATE {self.table} SET status = %s WHERE id = %s"
        result = db.execute(query, (status, report_id))
        db.close()
        return result is not None