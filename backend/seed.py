import random

from database import get_connection, init_db
from plates import get_region

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVXYZ"

MODELS = {
    "Sedan": ["Cobalt", "Nexia 3", "Gentra", "Lacetti", "Malibu", "Onix"],
    "Hatchback": ["Spark", "Matiz"],
    "SUV": ["Tracker", "Captiva", "Equinox", "BYD Song Plus"],
    "Miniven": ["Damas", "Orlando"],
    "Yuk mashinasi": ["Labo", "Isuzu NPR", "KAMAZ"],
    "Avtobus": ["Isuzu Citiport", "Yutong", "MAN Lion's City"],
}
WEIGHTS = [40, 20, 15, 10, 10, 5]


def random_plate():
    code = random.randint(1, 99)
    if random.random() < 0.85:
        return (f"{code:02d}{random.choice(LETTERS)}"
                f"{random.randint(0, 999):03d}"
                f"{random.choice(LETTERS)}{random.choice(LETTERS)}")
    return (f"{code:02d}{random.randint(0, 999):03d}"
            + "".join(random.choices(LETTERS, k=3)))


def seed(n=1000):
    init_db()
    types = list(MODELS.keys())
    added = 0
    with get_connection() as conn:
        while added < n:
            plate = random_plate()
            car_type = random.choices(types, weights=WEIGHTS)[0]
            model = random.choice(MODELS[car_type])
            cur = conn.execute(
                "INSERT OR IGNORE INTO cars (plate, region, car_type, model) "
                "VALUES (?, ?, ?, ?)",
                (plate, get_region(plate), car_type, model),
            )
            added += cur.rowcount
    print(f"{added} ta mashina qo'shildi")


if __name__ == "__main__":
    seed()