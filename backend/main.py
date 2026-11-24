import sqlite3
from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel

from database import get_connection, init_db
from plates import normalize, get_region

CAR_TYPES = ["Sedan", "Hatchback", "SUV", "Miniven", "Yuk mashinasi", "Avtobus"]
FRONTEND = Path(__file__).parent.parent / "frontend" / "index.html"

app = FastAPI(title="UZ Car Plates")
init_db()


# Frontend'dan keladigan ma'lumot shakli
class CarIn(BaseModel):
    plate: str
    car_type: str
    model: str = ""


def validate(car: CarIn):
    """Raqamni tekshiradi va (tozalangan raqam, viloyat) qaytaradi."""
    plate = normalize(car.plate)
    region = get_region(plate)
    if region is None:
        raise HTTPException(400, "Avtoraqam noto'g'ri formatda")
    if car.car_type not in CAR_TYPES:
        raise HTTPException(400, "Noma'lum mashina turi")
    return plate, region


@app.get("/")
def index():
    return FileResponse(FRONTEND)


@app.get("/api/types")
def get_types():
    return CAR_TYPES


# ---------- READ ----------
@app.get("/api/cars")
def list_cars(region: str | None = None, car_type: str | None = None):
    sql = "SELECT * FROM cars WHERE 1=1"
    params = []
    if region:
        sql += " AND region = ?"
        params.append(region)
    if car_type:
        sql += " AND car_type = ?"
        params.append(car_type)
    sql += " ORDER BY id DESC"
    with get_connection() as conn:
        rows = conn.execute(sql, params).fetchall()
    return [dict(r) for r in rows]


# ---------- CREATE ----------
@app.post("/api/cars", status_code=201)
def add_car(car: CarIn):
    plate, region = validate(car)
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "INSERT INTO cars (plate, region, car_type, model) VALUES (?, ?, ?, ?)",
                (plate, region, car.car_type, car.model),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Bu raqam bazada allaqachon bor")
    return {"id": cur.lastrowid, "plate": plate, "region": region,
            "car_type": car.car_type, "model": car.model}


# ---------- UPDATE ----------
@app.put("/api/cars/{car_id}")
def update_car(car_id: int, car: CarIn):
    plate, region = validate(car)
    try:
        with get_connection() as conn:
            cur = conn.execute(
                "UPDATE cars SET plate = ?, region = ?, car_type = ?, model = ? WHERE id = ?",
                (plate, region, car.car_type, car.model, car_id),
            )
    except sqlite3.IntegrityError:
        raise HTTPException(409, "Bu raqam bazada allaqachon bor")
    if cur.rowcount == 0:
        raise HTTPException(404, "Mashina topilmadi")
    return {"id": car_id, "plate": plate, "region": region,
            "car_type": car.car_type, "model": car.model}


# ---------- DELETE ----------
@app.delete("/api/cars/{car_id}")
def delete_car(car_id: int):
    with get_connection() as conn:
        cur = conn.execute("DELETE FROM cars WHERE id = ?", (car_id,))
    if cur.rowcount == 0:
        raise HTTPException(404, "Mashina topilmadi")
    return {"ok": True}


# ---------- STATISTIKA ----------
@app.get("/api/stats")
def stats():
    with get_connection() as conn:
        rows = conn.execute(
            "SELECT region, car_type, COUNT(*) AS n FROM cars GROUP BY region, car_type"
        ).fetchall()
    regions = {}
    types = {}
    for r in rows:
        reg = regions.setdefault(r["region"], {"total": 0, "types": {}})
        reg["total"] += r["n"]
        reg["types"][r["car_type"]] = r["n"]
        types[r["car_type"]] = types.get(r["car_type"], 0) + r["n"]
    return {"total": sum(types.values()), "regions": regions, "types": types}