import os
import sys
from fastapi import FastAPI

# Ensure the root directory is in the python path for Vercel
sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from app.api.endpoints import products
from app.db.session import engine, Base

# Initialize database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Expert Product Catalog API")

app.include_router(products.router, prefix="/products", tags=["products"])

@app.get("/")
def read_root():
    return {"status": "online", "message": "Expert Product Catalog API is running"}
