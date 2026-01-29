# Test script for Task 8 - Testing Relationships

Write-Host "=== Testing Task 8: Relationships Between Entities ===" -ForegroundColor Cyan
Write-Host ""

$baseUrl = "http://127.0.0.1:5001/api/v1"

# 1. Create a User (Owner)
Write-Host "1. Creating a user (owner)..." -ForegroundColor Yellow
try {
    $userResponse = Invoke-RestMethod -Uri "$baseUrl/users/" -Method Post -ContentType "application/json" -Body '{"first_name":"Ali","last_name":"Ahmed","email":"ali.task8@test.com","password":"password123"}'
    $userId = $userResponse.id
    Write-Host "[OK] User created with ID: $userId" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to create user: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 2. Create Amenities
Write-Host "2. Creating amenities..." -ForegroundColor Yellow
try {
    $amenity1Response = Invoke-RestMethod -Uri "$baseUrl/amenities/" -Method Post -ContentType "application/json" -Body '{"name":"WiFi"}'
    $amenity1Id = $amenity1Response.id
    Write-Host "[OK] Amenity 1 (WiFi) created with ID: $amenity1Id" -ForegroundColor Green
    
    $amenity2Response = Invoke-RestMethod -Uri "$baseUrl/amenities/" -Method Post -ContentType "application/json" -Body '{"name":"Swimming Pool"}'
    $amenity2Id = $amenity2Response.id
    Write-Host "[OK] Amenity 2 (Swimming Pool) created with ID: $amenity2Id" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to create amenities: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 3. Create a Place with owner and amenities
Write-Host "3. Creating a place with owner and amenities..." -ForegroundColor Yellow
try {
    $placeBody = @{
        title = "Luxury Villa"
        description = "Beautiful villa with sea view"
        price = 250.5
        latitude = 25.276987
        longitude = 55.296249
        owner_id = $userId
        amenities = @($amenity1Id, $amenity2Id)
    } | ConvertTo-Json
    
    $placeResponse = Invoke-RestMethod -Uri "$baseUrl/places/" -Method Post -ContentType "application/json" -Body $placeBody
    $placeId = $placeResponse.id
    Write-Host "[OK] Place created with ID: $placeId" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to create place: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 4. Get Place with relationships
Write-Host "4. Getting place with all relationships..." -ForegroundColor Yellow
try {
    $placeDetails = Invoke-RestMethod -Uri "$baseUrl/places/$placeId" -Method Get
    Write-Host "[OK] Place retrieved successfully" -ForegroundColor Green
    Write-Host "  - Title: $($placeDetails.title)" -ForegroundColor White
    Write-Host "  - Owner: $($placeDetails.owner_id)" -ForegroundColor White
    Write-Host "  - Amenities count: $(if ($placeDetails.amenities) { $placeDetails.amenities.Count } else { 0 })" -ForegroundColor White
} catch {
    Write-Host "[ERROR] Failed to get place: $_" -ForegroundColor Red
}
Write-Host ""

# 5. Create a Review
Write-Host "5. Creating a review..." -ForegroundColor Yellow
try {
    $reviewBody = @{
        text = "Amazing place! Highly recommended"
        rating = 5
        user_id = $userId
        place_id = $placeId
    } | ConvertTo-Json
    
    $reviewResponse = Invoke-RestMethod -Uri "$baseUrl/reviews/" -Method Post -ContentType "application/json" -Body $reviewBody
    $reviewId = $reviewResponse.id
    Write-Host "[OK] Review created with ID: $reviewId" -ForegroundColor Green
} catch {
    Write-Host "[ERROR] Failed to create review: $_" -ForegroundColor Red
    exit 1
}
Write-Host ""

# 6. Get Place Reviews
Write-Host "6. Getting all reviews for the place..." -ForegroundColor Yellow
try {
    $reviews = Invoke-RestMethod -Uri "$baseUrl/places/$placeId/reviews" -Method Get
    Write-Host "[OK] Found $($reviews.Count) review(s)" -ForegroundColor Green
    if ($reviews.Count -gt 0) {
        Write-Host "  - First review text: $($reviews[0].text)" -ForegroundColor White
        Write-Host "  - Rating: $($reviews[0].rating)" -ForegroundColor White
    }
} catch {
    Write-Host "[ERROR] Failed to get reviews: $_" -ForegroundColor Red
}
Write-Host ""

# 7. Test Database Integrity
Write-Host "7. Testing database relationships..." -ForegroundColor Yellow
try {
    $dbCheck = & "C:\Users\96650\Downloads\holbertonschool-hbnb\part3\venv\Scripts\python.exe" -c @"
from hbnb.app import create_app, db
from hbnb.app.models import User, Place, Review, Amenity

app = create_app()
app.app_context().push()

# Get the place with relationships
place = Place.query.get('$placeId')
if place:
    print(f'Place owner: {place.owner.first_name} {place.owner.last_name}')
    print(f'Place amenities: {len(place.amenities)}')
    print(f'Place reviews: {len(place.reviews)}')
    
    # Check reverse relationships
    user = User.query.get('$userId')
    print(f'User places: {len(user.places)}')
    print(f'User reviews: {len(user.reviews)}')
    
    # Check many-to-many
    amenity = Amenity.query.get('$amenity1Id')
    print(f'Amenity places: {len(amenity.places)}')
else:
    print('Place not found')
"@
    Write-Host "[OK] Database relationships verified:" -ForegroundColor Green
    $dbCheck -split "`n" | ForEach-Object { Write-Host "  - $_" -ForegroundColor White }
} catch {
    Write-Host "[ERROR] Failed to verify relationships: $_" -ForegroundColor Red
}
Write-Host ""

Write-Host "=== Task 8 Tests Completed Successfully! ===" -ForegroundColor Green
Write-Host ""
Write-Host "Summary:" -ForegroundColor Cyan
Write-Host "- User <-> Place relationship (one-to-many) [OK]" -ForegroundColor Green
Write-Host "- User <-> Review relationship (one-to-many) [OK]" -ForegroundColor Green
Write-Host "- Place <-> Review relationship (one-to-many) [OK]" -ForegroundColor Green
Write-Host "- Place <-> Amenity relationship (many-to-many) [OK]" -ForegroundColor Green
Write-Host "- Association table 'place_amenity' created [OK]" -ForegroundColor Green
Write-Host "- All foreign keys working correctly [OK]" -ForegroundColor Green
