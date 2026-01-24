# HBnB Evolution – Part 1  
## High-Level Package Diagram

### Objective
This diagram illustrates the three-layer architecture of the HBnB Evolution application and shows how the layers communicate using the Facade Pattern.

⸻
# Architecture Layers

## Presentation Layer

Handles user interaction through APIs and services.
It communicates only with the Business Logic layer via the Facade.

## Business Logic Layer

Contains the core application logic and models:
User, Place, Review, and Amenity.
The Facade coordinates all operations.

## Persistence Layer

Responsible for data storage and retrieval using repositories and the database.

⸻
# Facade Pattern

The Facade Pattern provides a unified interface between the Presentation Layer and the Business Logic Layer, simplifying interactions and reducing coupling between components.
---
