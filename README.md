# wound_clinic

This project is the backend of Wound Clinic built with FastAPI, SQLAlchemy, and PostgreSQL.
---

## Requirements

- Python 3.10+
- PostgreSQL 14+

## Installation
1. Clone the repository:
```bash
git clone https://github.com/yourusername/wound-clinic-backend.git
cd wound-clinic-backend
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate   # Linux/macOS
venv\Scripts\activate      # Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```
## Environment Variables
1. Create a .env file in the project root based on .env.example:
```bash
cp .env.example .env
```
2. Fill your .env
   
## Database Setup & Migration

1. Create your PostgreSQL database
   
Make sure alembic.ini has the correct sqlalchemy.url pointing to your database.

3. Initialize and run migrations:
```bash
alembic upgrade head
```
## Running the Project
Start the FastAPI development server:
```bash
fastapi dev main.py --reload
```

Open your browser at: http://127.0.0.1:8000/docs
