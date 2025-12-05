from pydantic import BaseModel, validator
from typing import Optional

class Vehicle(BaseModel):
    model_config = {"protected_namespaces": ()}

    vin: str
    manufacturer: str
    description: str
    horsepower: int
    model: str
    model_year: int
    purchase_price: float
    fuel_type: str



    @validator("*", pre=True)
    def no_nulls(cls, v):
        if v is None:
            raise ValueError("Field cannot be null")
        return v
