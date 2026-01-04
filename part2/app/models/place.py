from app.models.BaseEntity import BaseModel


class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Invalid name")
        if not price or price < 0:
            raise ValueError("Invalid name")
        if not latitude or latitude < -90.0 or latitude > 90.0:
            raise ValueError("Invalid number")
        if not longitude  or longitude  < -180.0 or longitude  > 180.0:
            raise ValueError("Invalid number")
        if not owner:
            raise ValueError("User does not exist")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []  # List to store related reviews
        self.amenities = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)
