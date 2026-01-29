"""Place Repository"""
from hbnb.app.models.place import Place
from hbnb.app.persistence.repository import SQLAlchemyRepository


class PlaceRepository(SQLAlchemyRepository):
    """Repository for Place entity with SQLAlchemy"""

    def __init__(self):
        super().__init__(Place)
