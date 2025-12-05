from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from schemas import Vehicle
import models
from database import initialize_db

app = FastAPI()
initialize_db()

@app.get("/")
def root():
    return {"status": "Vehicle API running"}

@app.exception_handler(ValueError)
async def value_error_handler(request: Request, exc: ValueError):
    return JSONResponse(
        status_code=422,
        content={"error": str(exc)}
    )

@app.get("/vehicle")
def get_vehicles():
    rows = models.get_all_vehicles()
    return [dict(row) for row in rows]


@app.post("/vehicle", status_code=201)
def create_vehicle(vehicle: Vehicle):
    existing = models.get_vehicle(vehicle.vin)
    if existing:
        raise HTTPException(status_code=422, detail="VIN already exists")

    models.create_vehicle(vehicle)
    return vehicle


@app.get("/vehicle/{vin}")
def get_vehicle(vin: str):
    row = models.get_vehicle(vin)
    if not row:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return dict(row)


@app.put("/vehicle/{vin}")
def update_vehicle(vin: str, vehicle: Vehicle):
    row = models.get_vehicle(vin)
    if not row:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    models.update_vehicle(vin, vehicle)
    return vehicle


@app.delete("/vehicle/{vin}", status_code=204)
def delete_vehicle(vin: str):
    row = models.get_vehicle(vin)
    if not row:
        raise HTTPException(status_code=404, detail="Vehicle not found")

    models.delete_vehicle(vin)
    return None
