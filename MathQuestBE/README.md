# MathQuest Backend (FastAPI + PostgreSQL + Pydantic)

Simple backend API for MathQuest web application.

## Initialized Database
```bash
docker compose up -d
```

## Create Virtual Environment (skip if already created)
```bash
python -m venv venv 
```

## Activate Virtual Environment and Install Dependencies
```bash
source venv/bin/activate
pip install -r requirements.txt
```

## Database Migrations
```bash
alembic upgrade head
```

## Seeding Data
```bash
python -m scripts.seed
```

## Run API (docs at /docs)
```bash
uvicorn app.main:app --reload --port 8000
```

## Run Unit Test
```bash
pytest -q
```