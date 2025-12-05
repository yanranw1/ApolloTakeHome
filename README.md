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

### 4. Data Model Table

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
