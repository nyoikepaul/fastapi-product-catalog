# Secure E-Commerce Product Catalog API

A professional, production-ready REST API built with **Python**, **FastAPI**, and **SQLAlchemy**. This project demonstrates industry best practices for modern backend development.

## 🚀 Key Features
* **Full CRUD Logic:** Create, Read, and Delete products with persistent SQLite storage.
* **Security:** API Key authentication for destructive operations (POST/DELETE).
* **Data Validation:** Strict type checking and validation using Pydantic schemas.
* **Documentation:** Automated interactive API documentation via Swagger UI.
* **Containerized:** Includes a Dockerfile for instant deployment across any cloud provider.

## 🛠️ Tech Stack
* **Backend:** FastAPI (Python 3.12)
* **Database:** SQLite with SQLAlchemy ORM
* **Deployment:** Docker, Uvicorn
* **Secrets:** Dotenv for environment variable management

## 📦 Getting Started
1. Clone the repo.
2. Create a `.env` file with `API_KEY=your_secret_here`.
3. Build the container: `docker build -t shop-api .`
4. Run: `docker run -p 8000:8000 --env-file .env shop-api`
