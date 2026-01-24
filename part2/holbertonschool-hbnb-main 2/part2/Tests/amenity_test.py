from app.models.amenity import Amenity

def test_amenity_creation():
    amenity = Amenity(name="Wi-Fi", places=[])
    assert amenity.name == "Wi-Fi"
    print("Amenity creation test passed!")
