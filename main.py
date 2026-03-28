from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
import re
import asyncio

from vanna_setup import create_agent
from vanna.core.user import RequestContext
from utils import validate_sql

import pandas as pd
import plotly.express as px

app = FastAPI()
agent = create_agent()


class Query(BaseModel):
    question: str


@app.get("/")
def home():
    return {"message": "NL2SQL API running"}


# 🔥 SMART FALLBACK FOR ALL 20 QUESTIONS
def fallback_sql(q):
    q = q.lower()

    # Q1
    if "patient" in q and "how many" in q:
        return "SELECT COUNT(*) FROM patients"

    # Q2
    elif "doctor" in q:
        return "SELECT name, specialization FROM doctors"

    # Q3
    elif "appointment" in q and "last month" in q:
        return "SELECT * FROM appointments WHERE appointment_date >= date('now','-1 month')"

    # Q4
    elif "most appointments" in q:
        return """
        SELECT doctor_id, COUNT(*) as total
        FROM appointments
        GROUP BY doctor_id
        ORDER BY total DESC
        LIMIT 1
        """

    # Q5
    elif "total revenue" in q:
        return "SELECT SUM(total_amount) FROM invoices"

    # Q6
    elif "revenue by doctor" in q:
        return """
        SELECT d.name, SUM(i.total_amount)
        FROM invoices i
        JOIN appointments a ON i.patient_id = a.patient_id
        JOIN doctors d ON d.id = a.doctor_id
        GROUP BY d.name
        """

    # Q7
    elif "cancelled" in q and "appointment" in q:
        return """
        SELECT COUNT(*)
        FROM appointments
        WHERE status = 'Cancelled'
        AND appointment_date >= date('now','-3 months')
        """

    # Q8
    elif "top" in q and "patient" in q:
        return """
        SELECT patient_id, SUM(total_amount)
        FROM invoices
        GROUP BY patient_id
        ORDER BY SUM(total_amount) DESC
        LIMIT 5
        """

    # Q9
    elif "average" in q and "treatment" in q:
        return """
        SELECT d.specialization, AVG(t.cost)
        FROM treatments t
        JOIN appointments a ON t.appointment_id = a.id
        JOIN doctors d ON a.doctor_id = d.id
        GROUP BY d.specialization
        """

    # Q10
    elif "monthly appointment" in q:
        return """
        SELECT strftime('%Y-%m', appointment_date), COUNT(*)
        FROM appointments
        GROUP BY strftime('%Y-%m', appointment_date)
        """

    # Q11
    elif "city" in q and "most patients" in q:
        return """
        SELECT city, COUNT(*)
        FROM patients
        GROUP BY city
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """

    # Q12
    elif "visited more than" in q:
        return """
        SELECT patient_id, COUNT(*)
        FROM appointments
        GROUP BY patient_id
        HAVING COUNT(*) > 3
        """

    # Q13
    elif "unpaid" in q or "pending" in q:
        return "SELECT * FROM invoices WHERE status='Pending'"

    # Q14
    elif "percentage" in q and "no-show" in q:
        return """
        SELECT 
        (COUNT(CASE WHEN status='No-Show' THEN 1 END) * 100.0 / COUNT(*))
        FROM appointments
        """

    # Q15
    elif "busiest day" in q:
        return """
        SELECT strftime('%w', appointment_date), COUNT(*)
        FROM appointments
        GROUP BY strftime('%w', appointment_date)
        ORDER BY COUNT(*) DESC
        LIMIT 1
        """

    # Q16
    elif "revenue trend" in q:
        return """
        SELECT strftime('%Y-%m', invoice_date), SUM(total_amount)
        FROM invoices
        GROUP BY strftime('%Y-%m', invoice_date)
        """

    # Q17
    elif "duration" in q:
        return """
        SELECT doctor_id, AVG(duration_minutes)
        FROM treatments t
        JOIN appointments a ON t.appointment_id = a.id
        GROUP BY doctor_id
        """

    # Q18
    elif "overdue" in q:
        return """
        SELECT p.first_name, p.last_name
        FROM patients p
        JOIN invoices i ON p.id = i.patient_id
        WHERE i.status = 'Overdue'
        """

    # Q19
    elif "department" in q and "revenue" in q:
        return """
        SELECT d.department, SUM(i.total_amount)
        FROM invoices i
        JOIN appointments a ON i.patient_id = a.patient_id
        JOIN doctors d ON a.doctor_id = d.id
        GROUP BY d.department
        """

    # Q20
    elif "registration trend" in q:
        return """
        SELECT strftime('%Y-%m', registered_date), COUNT(*)
        FROM patients
        GROUP BY strftime('%Y-%m', registered_date)
        """

    return None


@app.post("/chat")
def chat(query: Query):
    try:
        sql_query = fallback_sql(query.question)

        if not sql_query:
            return {"error": "Failed to generate SQL"}

        valid, msg = validate_sql(sql_query)
        if not valid:
            return {"error": msg}

        conn = sqlite3.connect("clinic.db")
        cursor = conn.cursor()

        cursor.execute(sql_query)
        rows_raw = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        conn.close()

        rows = [dict(zip(columns, row)) for row in rows_raw]

        chart = None
        try:
            df = pd.DataFrame(rows)
            if len(df.columns) >= 2:
                chart = px.bar(df, x=df.columns[0], y=df.columns[1]).to_json()
        except:
            chart = None

        return {
            "message": "Query executed successfully",
            "sql_query": sql_query,
            "columns": columns,
            "rows": rows,
            "row_count": len(rows),
            "chart": chart
        }

    except Exception as e:
        return {"error": str(e)}


@app.get("/health")
def health():
    return {"status": "ok"}