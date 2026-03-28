# AI-Powered NL2SQL System (Vanna 2.0 + FastAPI)

## 📌 Project Overview

This project implements a Natural Language to SQL (NL2SQL) system using Vanna AI 2.0 and FastAPI.

Users can ask questions in plain English, and the system:

* Converts it into SQL
* Executes it on a SQLite database
* Returns structured results and optional charts

---

## 🧠 Architecture

User Question
→ FastAPI Backend
→ Vanna 2.0 Agent (Gemini LLM + Tools)
→ SQL Validation
→ SQLite Database
→ Response (Rows + Columns + Chart)

---

## 🛠 Tech Stack

| Tool        | Purpose        |
| ----------- | -------------- |
| Python 3.11 | Backend        |
| FastAPI     | API Framework  |
| Vanna 2.0   | NL → SQL Agent |
| SQLite      | Database       |
| Gemini API  | LLM            |
| Plotly      | Charts         |

---

## ⚙️ Setup Instructions

### 1. Clone Repository

```bash
git clone <your_repo_link>
cd project
```

### 2. Create Virtual Environment

```bash
python -m venv venv
venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Add API Key

Create a `.env` file in the root directory:

```
GOOGLE_API_KEY=your_api_key_here
```

### 5. Create Database

```bash
python setup_database.py
```

### 6. (Optional) Seed Memory

```bash
python seed_memory.py
```

### 7. Run Server

```bash
uvicorn main:app --reload
```

Open API docs:

```
http://127.0.0.1:8000/docs
```

---

## 🚀 API Endpoints

### POST /chat

#### Request:

```json
{
  "question": "How many patients do we have?"
}
```

#### Response:

```json
{
  "message": "We have 200 patients.",
  "columns": ["count(*)"],
  "rows": [{"count(*)": 200}],
  "row_count": 1,
  "chart": null
}
```

---

### GET /health

#### Response:

```json
{
  "status": "ok"
}
```

---

## 📊 Features Implemented

* Natural Language → SQL conversion
* FastAPI backend
* SQLite database integration
* Structured API responses (columns, rows)
* Chart generation using Plotly
* SQL validation (basic safety checks)
* Async streaming handling (Vanna 2.0)

---

## ⚠️ Limitations

* SQL query is generated internally by Vanna and not always exposed
* Memory seeding is limited due to Vanna 2.0 API differences
* Complex queries (joins, aggregations) may not always be accurate
* SQL validation is basic and can be improved

---

## 🧪 Testing

The system was tested using 20 predefined questions as required in the assignment.

Example queries tested:

* How many patients do we have?
* List all doctors and their specializations
* Show revenue data
* Top cities by patient count

Detailed results are documented in `RESULTS.md`.

---

## 📁 Project Structure

```
project/
│
├── setup_database.py
├── seed_memory.py
├── vanna_setup.py
├── main.py
├──.env
├── utils.py
├── requirements.txt
├── README.md
├── RESULTS.md
├── clinic.db
```

---

## 👨‍💻 Author

Karthik

---

## 📌 Notes

* This project uses **Vanna AI 2.0 with Gemini LLM**
* SQLite is used for simplicity as per assignment requirements
* Memory seeding was partially implemented and documented due to API differences
* Focus was on building a stable, working end-to-end system
