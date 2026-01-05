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
