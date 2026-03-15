# FastAPI Product Catalog API

A modular, production-ready REST API built with FastAPI, SQLAlchemy 2.0, and Pydantic V2.

## 🚀 Features
- **Modular Architecture**: Clean separation of Models, Schemas, and Logic.
- **Database**: SQLAlchemy 2.0 with SQLite (local) and PostgreSQL support.
- **Security**: API Key header validation.
- **Testing**: 100% passing test suite with Pytest.

## 🛠️ Setup
1. `pip install -r requirements.txt`
2. `PYTHONPATH=. pytest` (Run tests)
3. `uvicorn app.main:app --reload` (Run locally)
