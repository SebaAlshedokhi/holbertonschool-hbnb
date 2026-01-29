# HBnB Database - Entity Relationship Diagram

## ER Diagram

```mermaid
erDiagram
    USER ||--o{ PLACE : owns
    USER ||--o{ REVIEW : writes
    PLACE ||--o{ REVIEW : has
    PLACE }o--o{ AMENITY : offers
    
    USER {
        char(36) id PK
        varchar(255) first_name
        varchar(255) last_name
        varchar(255) email UK
        varchar(255) password
        boolean is_admin
        timestamp created_at
        timestamp updated_at
    }
    
    PLACE {
        char(36) id PK
        varchar(255) title
        text description
        decimal(10_2) price
        float latitude
        float longitude
        char(36) owner_id FK
        timestamp created_at
        timestamp updated_at
    }
    
    REVIEW {
        char(36) id PK
        text text
        integer rating
        char(36) user_id FK
        char(36) place_id FK
        timestamp created_at
        timestamp updated_at
    }
    
    AMENITY {
        char(36) id PK
        varchar(255) name UK
        timestamp created_at
        timestamp updated_at
    }
    
    PLACE_AMENITY {
        char(36) place_id PK_FK
        char(36) amenity_id PK_FK
    }
```

---

## Relationships

### One-to-Many Relationships

1. **USER → PLACE**: A user can own multiple places, but each place has one owner
   - Cardinality: `||--o{` (one to zero or many)
   - Foreign Key: `PLACE.owner_id` references `USER.id`

2. **USER → REVIEW**: A user can write multiple reviews, but each review is written by one user
   - Cardinality: `||--o{` (one to zero or many)
   - Foreign Key: `REVIEW.user_id` references `USER.id`

3. **PLACE → REVIEW**: A place can have multiple reviews, but each review belongs to one place
   - Cardinality: `||--o{` (one to zero or many)
   - Foreign Key: `REVIEW.place_id` references `PLACE.id`

### Many-to-Many Relationship

4. **PLACE ↔ AMENITY**: A place can have many amenities, and an amenity can belong to many places
   - Cardinality: `}o--o{` (many to many)
   - Junction Table: `PLACE_AMENITY`
   - Foreign Keys: 
     - `PLACE_AMENITY.place_id` references `PLACE.id`
     - `PLACE_AMENITY.amenity_id` references `AMENITY.id`

---

## Cardinality Symbols

| Symbol | Meaning |
|--------|---------|
| `\|\|` | Exactly one |
| `o\|` | Zero or one |
| `}\|` | One or more |
| `}o` | Zero or more |

---

## Viewing the Diagram

- **Online Editor**: [Mermaid Live Editor](https://mermaid.live)
- **GitHub**: Automatically renders Mermaid diagrams in markdown files
