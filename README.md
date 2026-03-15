# FastAPI Product Catalog API

A modular, production-ready REST API built with **FastAPI**, **SQLAlchemy 2.0**, and **Pydantic V2**.

## 🚀 Key Features
* **Modular Architecture**: Clean separation of Models, Schemas, and API endpoints.
* **Modern ORM**: Utilizes SQLAlchemy 2.0's DeclarativeBase for future-proof data handling.
* **Security**: Integrated API Key validation for protected endpoints.
* **CI/CD**: Automated testing via GitHub Actions.

## 🛠️ Local Setup
1. **Clone the repo**: `git clone https://github.com/nyoikepaul/fastapi-product-catalog.git`
2. **Environment**: `python -m venv venv && source venv/bin/activate`
3. **Install**: `pip install -r requirements.txt`
4. **Test**: `PYTHONPATH=. pytest`
5. **Run**: `uvicorn app.main:app --reload`

