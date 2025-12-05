# Vehicle Service (CRUD API)

This project implements a simple CRUD-style REST API for managing vehicles.

## Tech Stack

- Python 3.10+
- FastAPI
- SQLite
- PyTest

## Running the Service

### 1. Install dependencies

`pip install -r requirements.txt`

### 2. Start the server

`uvicorn app:app --reload`

API will be available at:
http://localhost:8000

### 3. Run Tests

`pytest -v`

## API Endpoints

| Method | Endpoint         | Description        |
| ------ | ---------------- | ------------------ |
| GET    | `/vehicle`       | List all vehicles  |
| POST   | `/vehicle`       | Create new vehicle |
| GET    | `/vehicle/{vin}` | Get vehicle by VIN |
| PUT    | `/vehicle/{vin}` | Update vehicle     |
| DELETE | `/vehicle/{vin}` | Delete vehicle     |

## Validation Rules

- VIN must be unique (case-insensitive)
- All fields must be present (no nulls)
- Validation errors → `422 Unprocessable Entity`
- JSON parse errors → `400 Bad Request`

## Data Model Table

| Field            | Type    | Description                          |
| :--------------- | :------ | :----------------------------------- |
| `vin`            | String  | Unique Identifier (Case-insensitive) |
| `manufacturer`   | String  | Manufacturer Name                    |
| `description`    | String  | Vehicle Description                  |
| `horsepower`     | Integer | Horse Power                          |
| `model`          | String  | Model Name                           |
| `model_year`     | Integer | Year of the model                    |
| `purchase_price` | Float   | Price (Decimal)                      |
| `fuel_type`      | String  | Type of fuel                         |

## Project Structure and File Usage

| File                | Layer / Purpose                   | Description                                                                                                                                                                                         |
| ------------------- | --------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| app.py              | API Layer (Entry Point)           | Initializes the FastAPI application, sets up middleware, registers API routes (/vehicle), and defines global error handlers (for 422 validation and other exceptions).                              |
| schemas.py          | Data Layer (Validation)           | Contains the Pydantic Vehicle model, which defines the strict structure and data types for all incoming and outgoing vehicle data. Includes custom validation logic (e.g., preventing null values). |
| models.py           | Service Layer (CRUD Logic)        | Contains the core business logic functions (create_vehicle, get_vehicle, update_vehicle, delete_vehicle) that communicate directly with the database via database.py.                               |
| database.py         | Persistence Layer (DB Connection) | Handles the initialization of the SQLite database (vehicles.db) and provides a connection factory (get_connection) used by the models layer to execute SQL queries.                                 |
| test_vehicle_api.py | Testing Layer                     | Comprehensive test file using Pytest and FastAPI's TestClient to verify the functionality, error handling, and edge cases of every API endpoint.                                                    |
| requirements.txt    | Dependencies                      | Lists all required Python libraries (FastAPI, uvicorn, gunicorn, pytest, etc.) for easy setup via pip.                                                                                              |
