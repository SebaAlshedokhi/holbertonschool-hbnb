from __future__ import annotations

from typing import Any

from hbnb.app.models.base_model import BaseModel
from hbnb.app import db


class Amenity(BaseModel):
    """
    Amenity entity:
    - name (required, max 50)
    """
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name: str, **kwargs: Any):
        super().__init__(**kwargs)
        self.name = name
        self.validate()

    def validate(self) -> None:
        if not isinstance(self.name, str) or not self.name.strip():
            raise ValueError("name is required")
        if len(self.name) > 50:
            raise ValueError("name must be at most 50 characters")