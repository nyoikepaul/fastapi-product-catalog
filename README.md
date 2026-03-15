# 🚀 FastAPI Product Catalog

![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115.2-009688.svg)
![Tests](https://github.com/nyoikepaul/fastapi-product-catalog/actions/workflows/tests.yml/badge.svg)

A high-performance, modular Product Catalog API. Built for speed, security, and developer experience.

## 🛠 Quick Start
```bash
make install
make test
make docker-run  # App runs at http://localhost:8000
```

## 📌 API Endpoints
| Method | Endpoint | Description | Auth |
| :--- | :--- | :--- | :--- |
| GET | `/` | Health Check / Welcome | None |
| GET | `/products/` | List all products | None |
| POST | `/products/` | Create new product | API Key |

---
⭐ **Star this repo if you love clean, modular backends!**
