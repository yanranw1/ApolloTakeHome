from fastapi.testclient import TestClient
from app import app

client = TestClient(app)

# --- Test Data ---
sample_vehicle = {
    "vin": "TESTVIN123",
    "manufacturer": "Toyota",
    "description": "Compact car",
    "horsepower": 120,
    "model": "Corolla",
    "model_year": 2020,
    "purchase_price": 19000.50,
    "fuel_type": "Gas"
}

# --- Happy Path Tests (Standard CRUD) ---

def test_create_vehicle():
    # Cleanup in case previous run failed to delete
    client.delete("/vehicle/TESTVIN123")
    
    res = client.post("/vehicle", json=sample_vehicle)
    assert res.status_code == 201
    data = res.json()
    assert data["vin"] == "TESTVIN123"
    assert data["manufacturer"] == "Toyota"

def test_get_vehicle():
    res = client.get("/vehicle/TESTVIN123")
    assert res.status_code == 200
    assert res.json()["vin"] == "TESTVIN123"

def test_update_vehicle():
    update = sample_vehicle.copy()
    update["horsepower"] = 150
    update["description"] = "Turbo Edition"
    
    res = client.put("/vehicle/TESTVIN123", json=update)
    assert res.status_code == 200
    assert res.json()["horsepower"] == 150
    assert res.json()["description"] == "Turbo Edition"

def test_delete_vehicle():
    res = client.delete("/vehicle/TESTVIN123")
    assert res.status_code == 204
    
    # Verify it's actually gone
    res = client.get("/vehicle/TESTVIN123")
    assert res.status_code == 404

# --- Edge Case & Validation Tests ---

def test_create_duplicate_vin():
    # 1. Create a vehicle
    vin = "DUP123"
    vehicle = sample_vehicle.copy()
    vehicle["vin"] = vin
    
    # Clean up first to be safe
    client.delete(f"/vehicle/{vin}")
    client.post("/vehicle", json=vehicle)
    
    # 2. Try to create the same VIN again
    res = client.post("/vehicle", json=vehicle)
    
    # Should fail with 422 (Unprocessable Entity)
    assert res.status_code == 422
    assert "exists" in res.json()["detail"]
    
    # Cleanup
    client.delete(f"/vehicle/{vin}")

def test_get_non_existent_vehicle():
    res = client.get("/vehicle/IMAGINARY_CAR")
    assert res.status_code == 404
    assert res.json()["detail"] == "Vehicle not found"

def test_update_non_existent_vehicle():
    res = client.put("/vehicle/IMAGINARY_CAR", json=sample_vehicle)
    assert res.status_code == 404

def test_delete_non_existent_vehicle():
    res = client.delete("/vehicle/IMAGINARY_CAR")
    assert res.status_code == 404

def test_create_invalid_data_types():
    # Sending text for 'horsepower' (should be int)
    bad_vehicle = sample_vehicle.copy()
    bad_vehicle["vin"] = "BADTYPE"
    bad_vehicle["horsepower"] = "Not a number"
    
    res = client.post("/vehicle", json=bad_vehicle)
    assert res.status_code == 422

def test_create_missing_fields():
    # Payload missing 'model' and 'purchase_price'
    incomplete_vehicle = {
        "vin": "INCOMPLETE",
        "manufacturer": "Honda"
    }
    
    res = client.post("/vehicle", json=incomplete_vehicle)
    assert res.status_code == 422
    
def test_create_null_values():
    # Sending explicit null (None) for required fields
    null_vehicle = sample_vehicle.copy()
    null_vehicle["vin"] = "NULLTEST"
    null_vehicle["manufacturer"] = None
    
    res = client.post("/vehicle", json=null_vehicle)
    assert res.status_code == 422

def test_vin_case_insensitivity():
    # 1. Create with Mixed Case
    vin = "MixedCaseVin"
    vehicle = sample_vehicle.copy()
    vehicle["vin"] = vin
    
    client.delete(f"/vehicle/{vin}") # clean start
    client.post("/vehicle", json=vehicle)
    
    # 2. Try to GET using all lowercase
    res = client.get(f"/vehicle/{vin.lower()}")
    assert res.status_code == 200
    assert res.json()["vin"] == vin

    # 3. Try to GET using all uppercase
    res = client.get(f"/vehicle/{vin.upper()}")
    assert res.status_code == 200
    
    # Cleanup
    client.delete(f"/vehicle/{vin}")