# 🏠 HBnB Evolution – Technical Design Document (Enhanced Version)

## Table of Contents
1. [Introduction](#1-introduction)  
2. [High-Level Architecture](#2-high-level-architecture)  
   - 2.1 Architectural Overview  
   - 2.2 High-Level Package Diagram  
3. [Business Logic Layer – Class Diagram](#3-business-logic-layer--class-diagram)  
   - 3.1 Overview  
   - 3.2 Class Diagram  
   - 3.3 Design Rationale and Class Notes  
4. [API Interaction Flow – Sequence Diagrams](#4-api-interaction-flow--sequence-diagrams)  
   - 4.1 User Registration  
   - 4.2 Place Creation  
   - 4.3 Review Submission  
   - 4.4 Fetching List of Places  
5. [Conclusion](#5-conclusion)

---

## 1. Introduction

### 1.1 Purpose of This Document 📄
This document provides a **comprehensive architectural and design blueprint** for the HBnB Evolution application, a simplified AirBnB-like platform. It serves as a reference for developers, testers, and stakeholders during the implementation phases.

### 1.2 Scope 🎯
This document includes:  
- 🏗️ High-Level Architecture with **layer explanations and Facade Pattern rationale**  
- 📊 Detailed Class Diagram for the Business Logic layer with **per-class notes**  
- 🔄 Sequence Diagrams for key API interactions with **step-by-step explanations**  

---

## 2. High-Level Architecture

### 2.1 Architectural Overview 🏛️
HBnB Evolution is based on a **three-layer architecture**:

**Presentation Layer 🌐**  
- Exposes RESTful APIs  
- Handles HTTP requests/responses  
- Acts as **facade to Business Logic Layer**  

**Business Logic Layer ⚙️**  
- Core domain entities and business rules  
- Validates inputs and enforces constraints  

**Persistence Layer 💾**  
- Abstracts database operations  
- Stores and retrieves data efficiently  

**Rationale for Layering:**  
- Separation of concerns  
- Easier testing and maintenance  
- Flexibility for future extensions  

**Facade Pattern:**  
- `HBNBFacade` acts as a single interface to the Business Logic  
- Reduces complexity for the Presentation Layer  
- Encapsulates multiple operations (CRUD, validation) in one point of access  

---
### 2.2 High-Level Package Diagram 🗂️

```mermaid
classDiagram
    %% =======================
    %% Layers (Package View)
    %% =======================
    class PresentationLayer {
        <<Layer>>
        +API Endpoints
        +Services
    }

    class BusinessLogicLayer {
        <<Layer>>
        +HBNBFacade
        +Domain Models
        +Business Rules
    }

    class PersistenceLayer {
        <<Layer>>
        +Database Repositories
    }

    %% =======================
    %% Relationships
    %% =======================
    PresentationLayer --> BusinessLogicLayer : Uses Facade
    BusinessLogicLayer --> PersistenceLayer : CRUD Operations

```

**Notes 💡**  
- The **Presentation Layer** communicates only through the Facade.  
- The **Business Logic Layer** coordinates operations and delegates persistence tasks.  
- The **Persistence Layer** is independent of the Presentation Layer.  

---

## 3. Business Logic Layer – Class Diagram

### 3.1 Overview 🔹
Core entities:  
- 👤 **User** – represents platform users  
- 🏡 **Place** – represents property listings  
- ✍️ **Review** – user feedback  
- 🛏️ **Amenity** – features associated with a place  

**Key Features:**  
- UUID identifiers, timestamps  
- CRUD methods for API support  
- Relationships define ownership and aggregation  

---

### 3.2 Class Diagram 📊
```mermaid
classDiagram
  class BaseModel {
    +UUID id
    +datetime created_at
    +datetime updated_at
  }

  class User {
    +string first_name
    +string last_name
    +string email
    +string password
    +boolean is_admin
    +create()
    +update()
    +delete()
  }

  class Place {
    +string title
    +string description
    +float price
    +float latitude
    +float longitude
    +User owner
    +create()
    +update()
    +delete()
  }

  class Review {
    +int rating
    +string text
    +Place place
    +User user
    +create()
    +update()
    +delete()
  }

  class Amenity {
    +string name
    +create()
    +update()
    +delete()
  }

  BaseModel <|-- User
  BaseModel <|-- Place
  BaseModel <|-- Review
  BaseModel <|-- Amenity

  User "1" o-- "many" Place : owns
  User "1" o-- "many" Review : writes
  Place "1" o-- "many" Review : has
  Place "1" o-- "many" Amenity : includes

```

---

### 3.3 Design Rationale and Class Notes 💡

| Class  | Purpose | Notes |
|--------|---------|-------|
| BaseModel | Base for all entities | Provides `id`, `created_at`, `updated_at` |
| User | Platform user | Supports authentication; owns listings & reviews |
| Place | Property listing | Linked to User and Amenities; contains CRUD methods |
| Review | Feedback on Place | Connected to User and Place; rating & comment fields |
| Amenity | Features of Place | Many-to-many relationship with Place; flexible for future features |

**Relationships:**  
- **User → Place:** ownership of listings  
- **User → Review:** submission of reviews  
- **Place → Review:** multiple reviews per listing  
- **Place → Amenity:** allows multiple amenities per property  

---

## 4. API Interaction Flow – Sequence Diagrams

### 4.1 User Registration 📝
```mermaid
sequenceDiagram
    actor User
    participant API as API Service
    participant BL as Business Logic
    participant DB as Database

    User->>API: Create User
    API->>BL: create_user()
    BL->>BL: Validate user data

    alt User data valid
        BL->>DB: Save user data
        DB-->>BL: User created confirmation
        BL-->>API: User create successful
        API-->>User: HTTP 201 Created
    else User data invalid
        BL-->>API: Invalid user data request
        API-->>User: HTTP 400 Bad Request
    end

```

**Notes:**  
- Validation ensures email format, password strength  
- Database only receives validated data  

---

### 4.2 Place Creation 🏡
```mermaid

sequenceDiagram
    actor User
    participant API as API Service
    participant BL as Business Logic
    participant DB as Database

    User->>API: Create listing request
    API->>BL: create_listing(data)
    BL->>BL: Validate listing data

    alt Listing data valid
        BL->>DB: Save listing
        DB-->>BL: Listing save confirmation
        BL-->>API: Listing create successful
        API-->>User: HTTP 201 Created
    else Listing data invalid
        BL-->>API: Invalid data error
        API-->>User: HTTP 400 Bad Request
    end


```

**Notes:**  
- Validates listing data before saving  
- Ensures correct ownership by User  

---

### 4.3 Review Submission ✍️
```mermaid
sequenceDiagram
    actor User
    participant API as API Service
    participant BL as Business Logic
    participant DB as Database

    User->>API: Review Submission
    API->>BL: post_review()
    BL->>BL: Validate review data

    alt Review submission valid
        BL->>DB: Save Review
        DB-->>BL: Review stored confirmation
        BL-->>API: Review posted successful
        API-->>User: HTTP 201 Created
    else Review submission invalid
        BL-->>API: Review not valid
        API-->>User: HTTP 400 Bad Request
    end


```

**Notes:**  
- Allows users to submit feedback only for valid places  
- Validation of rating and comment required  

---

### 4.4 Fetching a List of Places 📋
```mermaid
sequenceDiagram
    actor User
    participant API as API Service
    participant BL as Business Logic
    participant DB as Database

    User->>API: Fetch place list request
    API->>BL: getPlaces()
    BL->>DB: Query all listings
    DB-->>BL: Return list of listings
    BL-->>API: Return place list
    API-->>User: HTTP 200 OK


```

**Notes:**  
- Supports optional filters for price, location, amenities  
- Returns structured JSON to the client  

---

## 5. Conclusion ✅
This document provides a **complete technical blueprint** for HBnB Evolution:  

- 🧹 Separation of concerns with layered architecture  
- 🛠️ Maintainable, extensible codebase  
- 🌟 Clear understanding of core entities, relationships, and API flows  
- ✅ Ready reference for developers and testers  
