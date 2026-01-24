# HBnB Project – Business Logic Layer

## Overview

This project implements the core **Business Logic layer** of the HBnB application.
The Business Logic layer is responsible for defining the domain entities, enforcing
business rules, validating data, and managing relationships between objects.

---

## Business Logic Layer

### Responsibilities

- Enforce domain rules and constraints
- Validate input data
- Manage relationships between entities
- Remain independent from the Presentation and Persistence layers

---

## BaseModel

All entities inherit from the `BaseModel` class.

### Responsibilities

- Generate a universally unique identifier (UUID)
- Track object creation time
- Track object update time

### Attributes

- `id`: String (UUID)
- `created_at`: DateTime
- `updated_at`: DateTime

### Example

```python
from app.models.base_model import BaseModel

base = BaseModel()
print(base.id)
print(base.created_at)
```

---

## Core Entities

### User

Represents a registered user in the system.

#### Responsibilities

- Store user information
- Own one or more places
- Write reviews

#### Attributes

- `first_name`: String
- `last_name`: String
- `email`: String
- `is_admin`: Boolean

#### Example

```python
from app.models.user import User

user = User(
    first_name="John",
    last_name="Doe",
    email="john.doe@example.com"
)
```

---

### Place

Represents a rentable place listed by a user.

#### Responsibilities

- Belong to a user (owner)
- Store location and pricing data
- Manage amenities
- Receive reviews

#### Attributes

- `title`: String
- `description`: String
- `price`: Float
- `latitude`: Float
- `longitude`: Float
- `owner`: User

#### Example

```python
from app.models.place import Place

place = Place(
    title="Cozy Apartment",
    description="Nice place",
    price=100.0,
    latitude=40.7,
    longitude=-74.0,
    owner=user
)
```

---

### Review

Represents a review written by a user for a place.

#### Responsibilities

- Validate review text
- Enforce rating range (1–5)
- Associate a user with a place

#### Attributes

- `text`: String
- `rating`: Integer
- `user`: User
- `place`: Place

#### Example

```python
from app.models.review import Review

review = Review(
    text="Great stay",
    rating=5,
    user=user,
    place=place
)
```

---

### Amenity

Represents an amenity associated with places.

#### Responsibilities

- Store amenity information
- Be linked to multiple places

#### Attributes

- `name`: String

#### Example

```python
from app.models.amenity import Amenity

wifi = Amenity(name="Wi-Fi")
place.add_amenity(wifi)
```

---

## Entity Relationships

- A User can own multiple Places (one-to-many)
- A Place can have multiple Reviews (one-to-many)
- A Review belongs to one User and one Place
- A Place can have multiple Amenities (many-to-many)

---

## Notes

- UUIDs are used to ensure global uniqueness
- All validations are handled in the Business Logic layer
- The layer is framework-agnostic and reusable

