# FastAPI Product Catalog

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.2-009688.svg)
![Tests](https://github.com/nyoikepaul/fastapi-product-catalog/actions/workflows/tests.yml/badge.svg)

A high-performance, modular Product Catalog API. Built for speed, security, and developer experience.

## Quick Start
bash
make install
make test
make docker-run  # App runs at http://localhost:8000

https://fastapi-product-catalog.vercel.app/redoc

## API Endpoints
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| GET | `/` | Health Check / Welcome | None |
| GET | `/products/` | List all products | None |
| POST | `/products/` | Create new product | API Key |
<img width="1366" height="600" alt="image" src="https://github.com/user-attachments/assets/3555907a-2665-4674-bf83-7ac75745c45a" />



---
⭐ **Star this repo if you love clean, modular backends!**

## Live Demo
🌐 **[fastapi-product-catalog.vercel.app](https://fastapi-product-catalog.vercel.app)**

## Tech Stack
| Layer | Tech |
|---|---|
| API | FastAPI 0.115 · Python 3.12 |
| Database | SQLite · SQLAlchemy |
| Auth | X-API-Key header |
| Deploy | Vercel · Docker |
| Tests | Pytest · GitHub Actions |
