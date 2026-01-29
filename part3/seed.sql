-- HBnB Initial Data
-- This script inserts the initial administrator user and default amenities

-- Insert Administrator User
-- Fixed UUID: 36c9050e-ddd3-4c3b-9731-9f487208bbc1
-- Email: admin@hbnb.io
-- Password: admin1234 (will be hashed by setup_database.py)
INSERT INTO users (id, first_name, last_name, email, password, is_admin, created_at, updated_at)
VALUES (
    '36c9050e-ddd3-4c3b-9731-9f487208bbc1',
    'Admin',
    'HBnB',
    'admin@hbnb.io',
    '$2b$12$HASH_WILL_BE_HERE',
    TRUE,
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- Insert Default Amenities

-- 1. WiFi
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'a1b2c3d4-e5f6-4a5b-9c8d-1e2f3a4b5c6d',
    'WiFi',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- 2. Swimming Pool
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'b2c3d4e5-f6a7-5b6c-ad9e-2f3a4b5c6d7e',
    'Swimming Pool',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);

-- 3. Air Conditioning
INSERT INTO amenities (id, name, created_at, updated_at)
VALUES (
    'c3d4e5f6-a7b8-6c7d-be0f-3a4b5c6d7e8f',
    'Air Conditioning',
    CURRENT_TIMESTAMP,
    CURRENT_TIMESTAMP
);
