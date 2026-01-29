"""Amenity Repository"""
from hbnb.app.models.amenity import Amenity
from hbnb.app.persistence.repository import SQLAlchemyRepository


class AmenityRepository(SQLAlchemyRepository):
    """Repository for Amenity entity with SQLAlchemy"""

    def __init__(self):
        super().__init__(Amenity)

    def get_by_name(self, name: str):
        """Get amenity by name"""
        return self.get_by_attribute('name', name)
