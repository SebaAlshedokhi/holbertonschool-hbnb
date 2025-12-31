from app.models.BaseEntity import BaseModel


class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first_name")
        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last_name")
        if not email:
            raise ValueError("Email required")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def add_review(self, text):
        """Add a text to the review."""
        self.text.append(text)
