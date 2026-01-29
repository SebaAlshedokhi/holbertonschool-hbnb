from hbnb.app import db
from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.user import User
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity

# Association table for many-to-many relationship between Place and Amenity
place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True)
)

__all__ = ["BaseModel", "User", "Place", "Review", "Amenity", "place_amenity"]