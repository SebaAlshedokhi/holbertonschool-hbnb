from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if user is None:
            return None

        for key, value in user_data.items():
            setattr(user, key, value)

        self.user_repo.update(user)
        return user



    # -------- AMENITY METHODS (Task 3) --------

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None
        for key, value in amenity_data.items():
            setattr(amenity, key, value)
            
        self.amenity_repo.update(amenity)
        return amenity


    # ----------- PLACE METHODS (Task 4) -----------

    def create_place(self, place_data):
        # Validate owner exists
        owner_id = place_data.get("owner_id")
        owner = self.user_repo.get(owner_id) if owner_id else None
        if owner is None:
            raise ValueError("Invalid owner_id")

        # Validate amenities exist (optional field but if given must be valid)
        amenities_ids = place_data.get("amenities", []) or []
        amenities_objs = []
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if amenity is None:
                raise ValueError("Invalid amenity_id")
            amenities_objs.append(amenity)

        # Validate numeric fields
        price = place_data.get("price")
        latitude = place_data.get("latitude")
        longitude = place_data.get("longitude")

        if price is None or price < 0:
            raise ValueError("Invalid price")
        if latitude is None or latitude < -90 or latitude > 90:
            raise ValueError("Invalid latitude")
        if longitude is None or longitude < -180 or longitude > 180:
            raise ValueError("Invalid longitude")
    
        # Create place
        place = Place(
            title=place_data.get("title"),
            description=place_data.get("description"),
            price=price,
            latitude=latitude,
            longitude=longitude,
            owner=owner
        )

        # Attach amenities
        for a in amenities_objs:
            place.add_amenity(a)

        self.place_repo.add(place)
        return place


    def get_place(self, place_id):
        return self.place_repo.get(place_id)


    def get_all_places(self):
        return self.place_repo.get_all()


    def update_place(self, place_id, place_data):
        place = self.place_repo.get(place_id)
        if place is None:
            return None

        # Only update allowed fields
        if "title" in place_data:
            place.title = place_data["title"]
        if "description" in place_data:
            place.description = place_data["description"]

        if "price" in place_data:
            if place_data["price"] is None or place_data["price"] < 0:
                raise ValueError("Invalid price")
            place.price = place_data["price"]

        if "latitude" in place_data:
            lat = place_data["latitude"]
            if lat is None or lat < -90 or lat > 90:
                raise ValueError("Invalid latitude")
            place.latitude = lat

        if "longitude" in place_data:
            lon = place_data["longitude"]
            if lon is None or lon < -180 or lon > 180:
                raise ValueError("Invalid longitude")
            place.longitude = lon

        # Update amenities if provided
        if "amenities" in place_data:
            amenities_ids = place_data.get("amenities") or []
            new_amenities = []
            for amenity_id in amenities_ids:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity is None:
                    raise ValueError("Invalid amenity_id")
                new_amenities.append(amenity)
            place.amenities = []
            for a in new_amenities:
                place.add_amenity(a)

        self.place_repo.update(place)
        return place
