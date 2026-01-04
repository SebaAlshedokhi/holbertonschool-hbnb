from app.models.BaseEntity import BaseModel


class Amenity(BaseModel):
    def __init__(self, name, places):
        super().__init__()

        if not name or len(name) > 50:
            raise ValueError("Invalid name")

        self.name = name
        self.places = []  # List to store related places

    def add_place(self, place):
        """Add a place to the user."""
        self.places.append(place)
