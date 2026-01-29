from __future__ import annotations

from typing import Any

from hbnb.app.models.base_model import BaseModel
from hbnb.app import db


class Place(BaseModel):
    """
    Place entity:
    - title (required, max 100)
    - description (optional)
    - price (positive float)
    - latitude  (-90..90)
    - longitude (-180..180)
    - owner_id (foreign key to User)
    Relationships: owner, reviews, amenities
    """
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=True, default="")
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationships
    reviews = db.relationship('Review', backref='place', lazy=True, cascade='all, delete-orphan')
    amenities = db.relationship('Amenity', secondary='place_amenity', lazy='subquery',
                                backref=db.backref('places', lazy=True))

    def __init__(
        self,
        title: str,
        price: float,
        latitude: float,
        longitude: float,
        owner_id: str,
        description: str = "",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id

        self.validate()

    def validate(self) -> None:
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title is required")
        if len(self.title) > 100:
            raise ValueError("title must be at most 100 characters")

        if not isinstance(self.description, str):
            raise ValueError("description must be a string")

        if not isinstance(self.price, (int, float)) or float(self.price) <= 0:
            raise ValueError("price must be a positive number")
        self.price = float(self.price)

        if not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number")
        if not (-90 <= float(self.latitude) <= 90):
            raise ValueError("latitude must be between -90 and 90")
        self.latitude = float(self.latitude)

        if not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number")
        if not (-180 <= float(self.longitude) <= 180):
            raise ValueError("longitude must be between -180 and 180")
        self.longitude = float(self.longitude)