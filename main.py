import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List
import models
from database import SessionLocal, engine
from pydantic import BaseModel

# 1. Load Environment Variables
load_dotenv()

# 2. Initialize Database
models.Base.metadata.create_all(bind=engine)

# 3. Security Config
API_KEY = os.getenv("API_KEY")
API_KEY_NAME = "access_token"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

app = FastAPI(
    title="Production-Ready API",
    description="Full CRUD API with JWT-style API Key Security and SQLite persistence."
)

# --- DEPENDENCIES ---

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_api_key(header_value: str = Security(api_key_header)):
    if header_value == API_KEY:
        return header_value
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Invalid or missing API Key. Check your .env file."
    )

# --- SCHEMAS ---

class ProductBase(BaseModel):
    name: str
    price: float
    description: str
    in_stock: bool = True

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# --- ROUTES ---

@app.get("/products/", response_model=List[ProductResponse])
def get_all_products(db: Session = Depends(get_db)):
    """Public: View all products."""
    return db.query(models.Product).all()

@app.post("/products/", response_model=ProductResponse)
def create_product(
    product: ProductBase, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Create a product (Requires API Key)."""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(
    product_id: int, 
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Delete a product (Requires API Key)."""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"message": f"Product {product_id} deleted successfully"}
