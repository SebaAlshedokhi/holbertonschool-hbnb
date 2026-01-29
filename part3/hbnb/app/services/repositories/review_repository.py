"""Review Repository"""
from hbnb.app.models.review import Review
from hbnb.app.persistence.repository import SQLAlchemyRepository


class ReviewRepository(SQLAlchemyRepository):
    """Repository for Review entity with SQLAlchemy"""

    def __init__(self):
        super().__init__(Review)
