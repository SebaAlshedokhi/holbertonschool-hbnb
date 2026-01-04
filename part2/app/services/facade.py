from app.persistence.repository import InMemoryRepository

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # Placeholder method for creating a user
    def create_user(self, user_data):
        exisiting_user = self.user_repo.get_by_attribute("email", user_data["email"])
        if exisiting_user:
            raise ValueError("Email already exists")

        user = User(**user_data)
        self.user_repo.add(user)

    return user

    # Placeholder method for fetching a place by ID
    def get_place(self, place_id):
        # Logic will be implemented in later tasks
        pass
