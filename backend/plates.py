import re

# (boshlanish kodi, tugash kodi, viloyat nomi)
REGIONS = [
    (1, 9, "Toshkent shahri"),
    (10, 19, "Toshkent viloyati"),
    (20, 24, "Sirdaryo"),
    (25, 29, "Jizzax"),
    (30, 39, "Samarqand"),
    (40, 49, "Farg'ona"),
    (50, 59, "Namangan"),
    (60, 69, "Andijon"),
    (70, 74, "Qashqadaryo"),
    (75, 79, "Surxondaryo"),
    (80, 84, "Buxoro"),
    (85, 89, "Navoiy"),
    (90, 94, "Xorazm"),
    (95, 99, "Qoraqalpog'iston"),
]

# Jismoniy shaxs:  01 A 123 BC  ->  01A123BC
PERSONAL = re.compile(r"^\d{2}[A-Z]\d{3}[A-Z]{2}$")
# Yuridik shaxs:   01 123 ABC   ->  01123ABC
LEGAL = re.compile(r"^\d{5}[A-Z]{3}$")


def normalize(plate):
    """Bo'sh joy va chiziqchalarni olib tashlab, katta harfga o'tkazadi."""
    return plate.replace(" ", "").replace("-", "").upper()


def is_valid(plate):
    p = normalize(plate)
    return bool(PERSONAL.match(p) or LEGAL.match(p))


def get_region(plate):
    """Raqam bo'yicha viloyat nomini qaytaradi, noto'g'ri bo'lsa None."""
    p = normalize(plate)
    if not is_valid(p):
        return None
    code = int(p[:2])
    for start, end, name in REGIONS:
        if start <= code <= end:
            return name
    return None


if __name__ == "__main__":
    tests = ["01 A 123 BC", "90 B 777 AA", "95 123 ABC",
             "40a555xx", "00 A 123 BC", "salom"]
    for t in tests:
        print(f"{t:15} -> {get_region(t)}")