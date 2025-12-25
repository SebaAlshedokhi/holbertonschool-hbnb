# HBnB Evolution - Technical Documentation

This document provides a complete overview of the HBnB Evolution application's architecture and business logic.

---

## 1. High-Level Package Diagram

This diagram illustrates the three-layer architecture (Presentation, Business Logic, Persistence) and how the layers communicate using the **Facade Pattern**.

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
    API --> HBNBFacade : Uses Facade
    Services --> HBNBFacade : Uses Facade
    HBNBFacade --> Repository : Interacts With
    Repository --> Database : Stores Data

    %% Models connected to Repository
    Repository --> User : Manages
    Repository --> Place : Manages
    Repository --> Review : Manages
    Repository --> Amenity : Manages
