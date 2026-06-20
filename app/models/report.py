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