import sqlite3
import random
from datetime import datetime, timedelta

conn = sqlite3.connect("clinic.db")
cursor = conn.cursor()

# 🔥 DROP OLD TABLES
cursor.executescript("""
DROP TABLE IF EXISTS patients;
DROP TABLE IF EXISTS doctors;
DROP TABLE IF EXISTS appointments;
DROP TABLE IF EXISTS invoices;
DROP TABLE IF EXISTS treatments;
""")

# 🔥 CREATE TABLES
cursor.executescript("""
CREATE TABLE patients (
    id INTEGER PRIMARY KEY,
    first_name TEXT,
    last_name TEXT,
    city TEXT,
    registered_date TEXT
);

CREATE TABLE doctors (
    id INTEGER PRIMARY KEY,
    name TEXT,
    specialization TEXT,
    department TEXT
);

CREATE TABLE appointments (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    doctor_id INTEGER,
    appointment_date TEXT,
    status TEXT
);

CREATE TABLE treatments (
    id INTEGER PRIMARY KEY,
    appointment_id INTEGER,
    cost REAL,
    duration_minutes INTEGER
);

CREATE TABLE invoices (
    id INTEGER PRIMARY KEY,
    patient_id INTEGER,
    total_amount REAL,
    status TEXT,
    invoice_date TEXT
);
""")

# 🔥 SAMPLE DATA
cities = ["Hyderabad", "Mumbai", "Delhi", "Bangalore"]
specializations = ["Cardiology", "Dermatology", "Orthopedics", "Pediatrics"]
departments = ["Heart", "Skin", "Bones", "Child"]
statuses = ["Completed", "Cancelled", "No-Show"]
invoice_status = ["Paid", "Pending", "Overdue"]

# 🔥 INSERT DOCTORS
for i in range(1, 11):
    cursor.execute(
        "INSERT INTO doctors VALUES (?, ?, ?, ?)",
        (
            i,
            f"Doctor_{i}",
            random.choice(specializations),
            random.choice(departments),
        ),
    )

# 🔥 INSERT PATIENTS
for i in range(1, 51):
    date = datetime.now() - timedelta(days=random.randint(0, 365))
    cursor.execute(
        "INSERT INTO patients VALUES (?, ?, ?, ?, ?)",
        (
            i,
            f"Patient_{i}",
            f"L{i}",
            random.choice(cities),
            date.strftime("%Y-%m-%d"),
        ),
    )

# 🔥 INSERT APPOINTMENTS
for i in range(1, 201):
    date = datetime.now() - timedelta(days=random.randint(0, 180))
    cursor.execute(
        "INSERT INTO appointments VALUES (?, ?, ?, ?, ?)",
        (
            i,
            random.randint(1, 50),
            random.randint(1, 10),
            date.strftime("%Y-%m-%d"),
            random.choice(statuses),
        ),
    )

# 🔥 INSERT TREATMENTS (LINKED)
for i in range(1, 201):
    cursor.execute(
        "INSERT INTO treatments VALUES (?, ?, ?, ?)",
        (
            i,
            i,  # same appointment_id
            random.randint(500, 5000),
            random.randint(15, 120),
        ),
    )

# 🔥 INSERT INVOICES
for i in range(1, 201):
    date = datetime.now() - timedelta(days=random.randint(0, 180))
    cursor.execute(
        "INSERT INTO invoices VALUES (?, ?, ?, ?, ?)",
        (
            i,
            random.randint(1, 50),
            random.randint(1000, 10000),
            random.choice(invoice_status),
            date.strftime("%Y-%m-%d"),
        ),
    )

conn.commit()
conn.close()

print("✅ Database created with strong sample data")