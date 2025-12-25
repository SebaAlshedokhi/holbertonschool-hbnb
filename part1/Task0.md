# HBnB Evolution - High-Level Architecture

This file shows the three layers in HBnB Evolution and the connection between them via **Facade Pattern**.

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
    class HBNBFacade {
        <<Facade>>
        %% Unified interface to interact with models
    }

    %% =======================
    %% Persistence Layer
    %% =======================
    class Repository {
        <<Persistence>>
        %% Manages data operations
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
    API --> HBNBFacade : Uses Facade
    Services --> HBNBFacade : Uses Facade
    HBNBFacade --> Repository : Interacts With
    Repository --> Database : Stores Data
