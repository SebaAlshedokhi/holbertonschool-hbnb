# HBnB System Architecture

هذا المخطط يوضح الطبقات المختلفة في نظام HBnB وكيفية تواصلها باستخدام **Facade Pattern**.

```mermaid
classDiagram
    %% Presentation Layer
    class API {
        <<Presentation>>
    }
    class Services {
        <<Presentation>>
    }

    %% Business Logic Layer
    class HBNBFacade {
        <<Facade>>
        +createUser()
        +getUser()
        +updateUser()
        +deleteUser()
        +createPlace()
        +getPlace()
        +updatePlace()
        +deletePlace()
        +createReview()
        +getReview()
        +updateReview()
        +deleteReview()
        +createAmenity()
        +getAmenity()
        +updateAmenity()
        +deleteAmenity()
    }

    %% Persistence Layer
    class Repository {
        <<Persistence>>
        +save()
        +get()
        +update()
        +delete()
    }
    class Database {
        <<Persistence>>
    }

    %% Models
    class User {
        <<Model>>
    }
    class Place {
        <<Model>>
    }
    class Review {
        <<Model>>
    }
    class Amenity {
        <<Model>>
    }

    %% Relationships
    API --> HBNBFacade : Uses Facade
    Services --> HBNBFacade : Uses Facade
    HBNBFacade --> Repository : CRUD Operations
    Repository --> Database : Stores Data
    Repository --> User : CRUD
    Repository --> Place : CRUD
    Repository --> Review : CRUD
    Repository --> Amenity : CRUD
