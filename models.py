from database import get_connection
from schemas import Vehicle


def create_vehicle(vehicle: Vehicle):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO vehicles (vin, manufacturer, description, horsepower, model, model_year, purchase_price, fuel_type)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            vehicle.vin,
            vehicle.manufacturer,
            vehicle.description,
            vehicle.horsepower,
            vehicle.model,
            vehicle.model_year,
            vehicle.purchase_price,
            vehicle.fuel_type
        ))
        conn.commit()


def get_all_vehicles():
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles")
        rows = cur.fetchall()
        return rows


def get_vehicle(vin: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("SELECT * FROM vehicles WHERE vin = ?", (vin,))
        row = cur.fetchone()
        return row


def update_vehicle(vin: str, vehicle: Vehicle):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE vehicles
            SET manufacturer=?, description=?, horsepower=?, model=?, model_year=?, purchase_price=?, fuel_type=?
            WHERE vin=?
        """, (
            vehicle.manufacturer,
            vehicle.description,
            vehicle.horsepower,
            vehicle.model,
            vehicle.model_year,
            vehicle.purchase_price,
            vehicle.fuel_type,
            vin,
        ))

        conn.commit()


def delete_vehicle(vin: str):
    with get_connection() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM vehicles WHERE vin = ?", (vin,))
        conn.commit()
