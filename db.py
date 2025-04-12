import sqlite3
from datetime import datetime, timedelta

def init_db():
    conn = sqlite3.connect("car_service.db")
    cur = conn.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT,
        car TEXT,
        plate TEXT,
        phone TEXT,
        km INTEGER,
        last_service TEXT,
        chat_id INTEGER
    )''')
    conn.commit()
    conn.close()

def add_user(name, car, plate, phone, km, last_service, chat_id=None):
    conn = sqlite3.connect("car_service.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO users (name, car, plate, phone, km, last_service, chat_id) VALUES (?, ?, ?, ?, ?, ?, ?)",
                (name, car, plate, phone, km, last_service, chat_id))
    conn.commit()
    conn.close()

def get_due_services():
    conn = sqlite3.connect("car_service.db")
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    now = datetime.now()
    date_threshold = now - timedelta(days=60)
    km_threshold = 5000
    cur.execute("SELECT * FROM users WHERE km >= ? OR last_service <= ?", (km_threshold, date_threshold.strftime("%Y-%m-%d")))
    results = cur.fetchall()
    conn.close()
    return results