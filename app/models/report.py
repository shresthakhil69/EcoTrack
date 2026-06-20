from app.models.base import BaseModel

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

