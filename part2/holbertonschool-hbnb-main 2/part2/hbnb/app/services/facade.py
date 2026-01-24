from hbnb.app.persistence.repository import InMemoryRepository
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ===== User Management Methods =====

    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_all_users(self):
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        user = self.user_repo.get(user_id)
        if not user:
            return None

        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        if 'is_admin' in user_data:
            user.is_admin = user_data['is_admin']

        user.validate()
        user.save()
        return user

    # ===== Place Management Methods =====

    def create_place(self, place_data):
        """Create a new place with validation"""

        # ---- price validation ----
        if place_data['price'] < 0:
            raise ValueError("Price must be positive")

        # ---- latitude validation ----
        if not -90 <= place_data['latitude'] <= 90:
            raise ValueError("Invalid latitude")

        # ---- longitude validation ----
        if not -180 <= place_data['longitude'] <= 180:
            raise ValueError("Invalid longitude")

        # ---- owner validation ----
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        # ---- amenities validation ----
        amenities_ids = place_data.get('amenities', [])
        for amenity_id in amenities_ids:
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError("Invalid amenity ID")
            place.add_amenity(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update place (owner cannot be changed)"""

        place = self.place_repo.get(place_id)
        if not place:
            raise LookupError("Place not found")

        if 'price' in place_data:
            if place_data['price'] < 0:
                raise ValueError("Price must be positive")
            place.price = place_data['price']

        if 'latitude' in place_data:
            if not -90 <= place_data['latitude'] <= 90:
                raise ValueError("Invalid latitude")
            place.latitude = place_data['latitude']

        if 'longitude' in place_data:
            if not -180 <= place_data['longitude'] <= 180:
                raise ValueError("Invalid longitude")
            place.longitude = place_data['longitude']

        if 'title' in place_data:
            place.title = place_data['title']

        if 'description' in place_data:
            place.description = place_data['description']

        # ❌ owner_id MUST NOT be updated

        if 'amenities' in place_data:
            place.amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError("Invalid amenity ID")
                place.add_amenity(amenity)

        place.save()
        return place

    # ===== Amenity Management Methods =====

    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        return self.amenity_repo.get_by_attribute('name', name)

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        if 'name' in amenity_data:
            amenity.name = amenity_data['name']

        amenity.validate()
        amenity.save()
        return amenity

    # ===== Review Management Methods (unchanged – next task) =====

    def create_review(self, review_data):
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )

        self.review_repo.add(review)
        return review
