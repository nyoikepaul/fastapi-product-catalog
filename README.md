

# Secure Product Catalog API 

Production-ready FastAPI product catalog with **full CRUD**, validation, pagination, and `X-API-Key` security.

## 🚀 Features
- ✅ **Full CRUD** + pagination (`?skip=0&limit=10`)
- ✅ Pydantic `Field` validation (`price > 0`, name length, etc.)
- ✅ `X-API-Key` header security (clean Swagger UI)
- ✅ Vercel + Docker ready (zero-downtime)
- ✅ Production-grade code (pinned deps, proper 204 DELETE, etc.)

## 📡 Live Demo
https://fastapi-product-catalog.vercel.app/docs#/

## 🛠 Quick Start (Local)
```bash
cp .env.example .env          # ← set your API_KEY
docker build -t shop-api .
docker run -p 8000:8000 --env-file .env shop-api

Open http://localhost:8000/docs
