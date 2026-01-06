from app.models.BaseEntity import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Text required")
        if rating < 1 or rating > 5:
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(place, Place):
            raise TypeError("place must be a valid Place instance")
        if not isinstance(user, User):
            raise TypeError("user must be a valid User instance")
            
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
