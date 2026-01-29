from hbnb.app.services.repositories.user_repository import UserRepository
from hbnb.app.services.repositories.place_repository import PlaceRepository
from hbnb.app.services.repositories.review_repository import ReviewRepository
from hbnb.app.services.repositories.amenity_repository import AmenityRepository
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review


class HBnBFacade:
    """
    Facade pattern implementation for the HBnB application.
    Uses singleton pattern to ensure all endpoints share the same repositories.
    """
    _instance = None
    _repositories_initialized = False
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(HBnBFacade, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Only initialize repositories once
        if not HBnBFacade._repositories_initialized:
            # Use SQLAlchemy repositories (Tasks 6 & 7)
            self.user_repo = UserRepository()
            self.place_repo = PlaceRepository()
            self.review_repo = ReviewRepository()
            self.amenity_repo = AmenityRepository()
            HBnBFacade._repositories_initialized = True

    # ===== User Management Methods =====

    def create_user(self, user_data):
        """Create a new user"""
        # Extract password before creating user instance
        password = user_data.pop('password', None)
        user = User(**user_data)
        if password:
            user.hash_password(password)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_repo.get_user_by_email(email)

    def update_user(self, user_id, user_data):
        """Update a user's information"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Update user attributes
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        if 'is_admin' in user_data:
            user.is_admin = user_data['is_admin']

        # Validate the updated user
        user.validate()
        user.save()

        # Update in repository
        self.user_repo.update(user_id, user_data)
        return user

    # ===== Place Management Methods =====

    def create_place(self, place_data):
        """Create a new place with owner and amenities"""
        # Validate owner exists
        owner = self.user_repo.get(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")

        # Create place with owner_id
        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=place_data['owner_id']
        )

        # Add amenities if provided
        if 'amenities' in place_data and place_data['amenities']:
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Get a place by ID"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Get all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Update a place's information"""
        place = self.place_repo.get(place_id)
        if not place:
            return None

        # Update basic attributes
        if 'title' in place_data:
            place.title = place_data['title']
        if 'description' in place_data:
            place.description = place_data['description']
        if 'price' in place_data:
            place.price = place_data['price']
        if 'latitude' in place_data:
            place.latitude = place_data['latitude']
        if 'longitude' in place_data:
            place.longitude = place_data['longitude']

        # Update owner if provided
        if 'owner_id' in place_data:
            owner = self.user_repo.get(place_data['owner_id'])
            if not owner:
                raise ValueError("Owner not found")
            place.owner_id = place_data['owner_id']

        # Update amenities if provided
        if 'amenities' in place_data:
            place.amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.amenity_repo.get(amenity_id)
                if amenity:
                    place.amenities.append(amenity)

        # Validate and save
        place.validate()
        place.save()

        # Update in repository
        self.place_repo.update(place_id, place_data)
        return place

    # ===== Amenity Management Methods =====

    def create_amenity(self, amenity_data):
        """Create a new amenity"""
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        """Get an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Get all amenities"""
        return self.amenity_repo.get_all()

    def get_amenity_by_name(self, name):
        """Get an amenity by name"""
        return self.amenity_repo.get_by_attribute('name', name)

    def update_amenity(self, amenity_id, amenity_data):
        """Update an amenity's information"""
        amenity = self.amenity_repo.get(amenity_id)
        if not amenity:
            return None

        # Update amenity attributes
        if 'name' in amenity_data:
            amenity.name = amenity_data['name']

        # Validate the updated amenity
        amenity.validate()
        amenity.save()

        # Update in repository
        self.amenity_repo.update(amenity_id, amenity_data)
        return amenity

    # ===== Review Management Methods =====

    def create_review(self, review_data):
        """Create a new review"""
        # Validate that user and place exist
        user = self.user_repo.get(review_data['user_id'])
        if not user:
            raise ValueError("User not found")

        place = self.place_repo.get(review_data['place_id'])
        if not place:
            raise ValueError("Place not found")

        # Create review with relationships
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=review_data['user_id'],
            place_id=review_data['place_id']
        )

        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Get a review by ID"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Get all reviews"""
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        place = self.place_repo.get(place_id)
        if not place:
            return []
        return place.reviews  # Now works with relationships!

    def update_review(self, review_id, review_data):
        """Update a review's information"""
        review = self.review_repo.get(review_id)
        if not review:
            return None

    def update_review(self, review_id, review_data):
        """Update a review's information"""
        review = self.review_repo.get(review_id)
        if not review:
            return None

        # Update basic attributes
        if 'text' in review_data:
            review.text = review_data['text']
        if 'rating' in review_data:
            review.rating = review_data['rating']

        # Validate and update user_id if provided
        if 'user_id' in review_data:
            user = self.user_repo.get(review_data['user_id'])
            if not user:
                raise ValueError("User not found")
            review.user_id = review_data['user_id']

        # Validate and update place_id if provided
        if 'place_id' in review_data:
            place = self.place_repo.get(review_data['place_id'])
            if not place:
                raise ValueError("Place not found")
            review.place_id = review_data['place_id']

        # Validate and save
        review.validate()
        review.save()

        # Update in repository
        self.review_repo.update(review_id, review_data)
        return review

    def delete_review(self, review_id):
        """Delete a review"""
        review = self.review_repo.get(review_id)
        if review:
            self.review_repo.delete(review_id)
            return True
        return False
