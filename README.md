\# 🚗 O'zbekiston avtoraqamlari



Avtomobil raqami orqali uning qaysi viloyatga tegishli ekanini aniqlaydigan veb-ilova.



\## Imkoniyatlar

\- Raqamdan viloyatni avtomatik aniqlash (`01 A 123 BC` → Toshkent shahri)

\- Mashinalarni qo'shish, tahrirlash va o'chirish (CRUD)

\- Asosiy ekranda O'zbekiston xaritasi: viloyat bosilganda undagi mashinalar soni chiqadi

\- Mashinalarni turi bo'yicha guruhlash (Sedan, SUV, Avtobus...)

\- Bazada 1000 ta tasodifiy o'zbek avtoraqami



\## Texnologiyalar

\- \*\*Backend:\*\* Python, FastAPI, SQLite

\- \*\*Frontend:\*\* HTML, CSS, JavaScript, Highcharts Maps



\## Viloyat kodlari

| Kod | Viloyat | Kod | Viloyat |

|---|---|---|---|

| 01–09 | Toshkent shahri | 50–59 | Namangan |

| 10–19 | Toshkent viloyati | 60–69 | Andijon |

| 20–24 | Sirdaryo | 70–74 | Qashqadaryo |

| 25–29 | Jizzax | 75–79 | Surxondaryo |

| 30–39 | Samarqand | 80–84 | Buxoro |

| 40–49 | Farg'ona | 85–89 | Navoiy |

| 90–94 | Xorazm | 95–99 | Qoraqalpog'iston |



\## Ishga tushirish

```bash

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt

python backend/seed.py

uvicorn main:app --reload --app-dir backend

```

Brauzerda oching: http://127.0.0.1:8000



\## Muallif

Javohir Jumanazarov

