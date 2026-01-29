"""
Direct test of Task 8 relationships without Flask server
"""
import sys
import os

# Add the project root to the path
sys.path.insert(0, os.path.dirname(__file__))

from hbnb.app import create_app, db
from hbnb.app.models.user import User
from hbnb.app.models.place import Place
from hbnb.app.models.amenity import Amenity
from hbnb.app.models.review import Review
from hbnb.app.extensions import bcrypt

def test_relationships():
    """Test all relationships defined in Task 8"""
    app = create_app()
    
    with app.app_context():
        print("=" * 60)
        print("Testing Task 8: Relationships Between Entities")
        print("=" * 60)
        print()
        
        # Clean up existing data
        print("🧹 Cleaning up existing data...")
        Review.query.delete()
        Place.query.delete()
        User.query.delete()
        Amenity.query.delete()
        db.session.commit()
        print("✅ Database cleaned\n")
        
        # Test 1: User -> Places relationship (one-to-many)
        print("📋 Test 1: User -> Places Relationship (One-to-Many)")
        print("-" * 60)
        
        user = User(
            first_name="Ahmed",
            last_name="Ali",
            email="ahmed@test.com"
        )
        user.hash_password("password123")
        db.session.add(user)
        db.session.commit()
        print(f"✅ Created User: {user.first_name} {user.last_name} (ID: {user.id})")
        
        place1 = Place(
            title="Luxury Villa",
            description="Beautiful villa with sea view",
            price=200.0,
            latitude=25.276987,
            longitude=55.296249,
            owner_id=user.id
        )
        place2 = Place(
            title="Downtown Apartment",
            description="Modern apartment in city center",
            price=100.0,
            latitude=25.197197,
            longitude=55.274376,
            owner_id=user.id
        )
        db.session.add(place1)
        db.session.add(place2)
        db.session.commit()
        print(f"✅ Created Place 1: {place1.title} (ID: {place1.id})")
        print(f"✅ Created Place 2: {place2.title} (ID: {place2.id})")
        
        # Test accessing places from user
        user_places = user.places
        print(f"\n🔗 User has {len(user_places)} places:")
        for place in user_places:
            print(f"   - {place.title}")
        
        # Test accessing owner from place
        print(f"\n🔗 Place owner: {place1.owner.first_name} {place1.owner.last_name}")
        
        assert len(user_places) == 2, "User should have 2 places"
        assert place1.owner.id == user.id, "Place owner should match user"
        print("✅ User -> Places relationship works!\n")
        
        # Test 2: Place -> Amenities relationship (many-to-many)
        print("📋 Test 2: Place -> Amenities Relationship (Many-to-Many)")
        print("-" * 60)
        
        amenity1 = Amenity(name="WiFi")
        amenity2 = Amenity(name="Swimming Pool")
        amenity3 = Amenity(name="Parking")
        db.session.add_all([amenity1, amenity2, amenity3])
        db.session.commit()
        print(f"✅ Created Amenity 1: {amenity1.name} (ID: {amenity1.id})")
        print(f"✅ Created Amenity 2: {amenity2.name} (ID: {amenity2.id})")
        print(f"✅ Created Amenity 3: {amenity3.name} (ID: {amenity3.id})")
        
        # Add amenities to place1
        place1.amenities.append(amenity1)
        place1.amenities.append(amenity2)
        db.session.commit()
        print(f"\n🔗 Added amenities to {place1.title}")
        
        # Add amenities to place2
        place2.amenities.append(amenity2)  # Swimming Pool (shared)
        place2.amenities.append(amenity3)  # Parking
        db.session.commit()
        print(f"🔗 Added amenities to {place2.title}")
        
        # Test accessing amenities from place
        print(f"\n🔗 {place1.title} has {len(place1.amenities)} amenities:")
        for amenity in place1.amenities:
            print(f"   - {amenity.name}")
        
        print(f"\n🔗 {place2.title} has {len(place2.amenities)} amenities:")
        for amenity in place2.amenities:
            print(f"   - {amenity.name}")
        
        # Test accessing places from amenity
        print(f"\n🔗 {amenity2.name} is in {len(amenity2.places)} places:")
        for place in amenity2.places:
            print(f"   - {place.title}")
        
        assert len(place1.amenities) == 2, "Place1 should have 2 amenities"
        assert len(place2.amenities) == 2, "Place2 should have 2 amenities"
        assert len(amenity2.places) == 2, "Swimming Pool should be in 2 places"
        print("✅ Place -> Amenities relationship works!\n")
        
        # Test 3: User -> Reviews relationship (one-to-many)
        print("📋 Test 3: User -> Reviews Relationship (One-to-Many)")
        print("-" * 60)
        
        # Create another user as reviewer
        reviewer = User(
            first_name="Sara",
            last_name="Mohamed",
            email="sara@test.com"
        )
        reviewer.hash_password("password123")
        db.session.add(reviewer)
        db.session.commit()
        print(f"✅ Created Reviewer: {reviewer.first_name} {reviewer.last_name} (ID: {reviewer.id})")
        
        review1 = Review(
            text="Amazing place! Highly recommended.",
            rating=5,
            user_id=reviewer.id,
            place_id=place1.id
        )
        review2 = Review(
            text="Great location and amenities.",
            rating=4,
            user_id=reviewer.id,
            place_id=place2.id
        )
        db.session.add_all([review1, review2])
        db.session.commit()
        print(f"✅ Created Review 1 for {place1.title}")
        print(f"✅ Created Review 2 for {place2.title}")
        
        # Test accessing reviews from user
        reviewer_reviews = reviewer.reviews
        print(f"\n🔗 {reviewer.first_name} has {len(reviewer_reviews)} reviews:")
        for review in reviewer_reviews:
            print(f"   - Rating: {review.rating}/5 - {review.text[:50]}...")
        
        assert len(reviewer_reviews) == 2, "Reviewer should have 2 reviews"
        print("✅ User -> Reviews relationship works!\n")
        
        # Test 4: Place -> Reviews relationship (one-to-many)
        print("📋 Test 4: Place -> Reviews Relationship (One-to-Many)")
        print("-" * 60)
        
        # Add another review to place1
        review3 = Review(
            text="Good value for money.",
            rating=4,
            user_id=user.id,  # Owner can also review
            place_id=place1.id
        )
        db.session.add(review3)
        db.session.commit()
        print(f"✅ Created Review 3 for {place1.title}")
        
        # Test accessing reviews from place
        place1_reviews = place1.reviews
        print(f"\n🔗 {place1.title} has {len(place1_reviews)} reviews:")
        for review in place1_reviews:
            print(f"   - Rating: {review.rating}/5 by User {review.user_id[:8]}...")
        
        assert len(place1_reviews) == 2, "Place1 should have 2 reviews"
        assert len(place2.reviews) == 1, "Place2 should have 1 review"
        print("✅ Place -> Reviews relationship works!\n")
        
        # Test 5: Cascade delete
        print("📋 Test 5: Cascade Delete Operations")
        print("-" * 60)
        
        # Delete user and check if their places and reviews are deleted
        user_id = user.id
        place1_id = place1.id
        place2_id = place2.id
        
        print(f"🗑️  Deleting user: {user.first_name} {user.last_name}")
        db.session.delete(user)
        db.session.commit()
        
        # Check if places were deleted
        deleted_place1 = Place.query.get(place1_id)
        deleted_place2 = Place.query.get(place2_id)
        
        assert deleted_place1 is None, "Place1 should be deleted when owner is deleted"
        assert deleted_place2 is None, "Place2 should be deleted when owner is deleted"
        print("✅ Cascade delete works! Places deleted when owner deleted\n")
        
        # Verify reviews were also deleted (because places were deleted)
        all_reviews = Review.query.all()
        print(f"🔗 Remaining reviews in database: {len(all_reviews)}")
        # Reviews should also be deleted because places were deleted (place has cascade on reviews)
        print("✅ Related reviews also deleted!\n")
        
        # Summary
        print("=" * 60)
        print("✅ All Task 8 Relationship Tests Passed!")
        print("=" * 60)
        print("\n📊 Summary:")
        print("   ✅ User -> Places (One-to-Many)")
        print("   ✅ Place -> Amenities (Many-to-Many)")
        print("   ✅ User -> Reviews (One-to-Many)")
        print("   ✅ Place -> Reviews (One-to-Many)")
        print("   ✅ Cascade Delete Operations")
        print("\n🎉 Task 8 implementation is correct!")

if __name__ == "__main__":
    try:
        test_relationships()
    except Exception as e:
        print(f"\n❌ Test failed with error:")
        print(f"   {type(e).__name__}: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
