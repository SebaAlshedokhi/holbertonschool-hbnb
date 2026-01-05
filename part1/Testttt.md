```mermaid

classDiagram
    %% =======================
    %% Presentation Layer
    %% =======================
    class API {
        <<Presentation>>
        %% Handles user requests via endpoints
    }
    class Services {
        <<Presentation>>
        %% Provides service logic for API
    }

    %% =======================
    %% Business Logic Layer
    %% =======================
    class BusinessLogicLayer {
        <<Layer>>
        +HBNBFacade
        +Domain Models
        +Business Rules
    }

    %% =======================
    %% Persistence Layer
    %% =======================
    class Repository {
        <<Persistence>>
        %% Manages data operations for models
    }
    class Database {
        <<Persistence>>
        %% Stores application data
    }

    %% =======================
    %% Models
    %% =======================
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

    %% =======================
    %% Relationships
    %% =======================

    API --> BusinessLogicLayer : Uses Facade
    Services --> BusinessLogicLayer : Uses Facade
    BusinessLogicLayer --> Repository : Interacts With
    Repository --> Database : Stores Data
    
    %% Models connected to Repository
    Repository --> User : Manages
    Repository --> Place : Manages
    Repository --> Review : Manages
    Repository --> Amenity : Manages

