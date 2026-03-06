import os
from dotenv import load_dotenv
from fastapi import FastAPI, Depends, HTTPException, Security, status, Query, Response
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel, Field

import models
from database import SessionLocal, engine

load_dotenv()

# Create tables on startup
models.Base.metadata.create_all(bind=engine)

# ================== APP ==================
app = FastAPI(
    title="FastAPI Product Catalog",
    description="Expert-level production API • Full CRUD • Validation • Pagination • X-API-Key",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

# ================== SECURITY ==================
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise RuntimeError("❌ API_KEY missing in .env — add it!")

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

# ================== DB ==================
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(status_code=403, detail="Invalid or missing X-API-Key")

# ================== SCHEMAS ==================
class ProductBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    price: float = Field(..., gt=0.0)
    description: str = Field(..., min_length=1)
    in_stock: bool = True

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    price: Optional[float] = Field(None, gt=0.0)
    description: Optional[str] = Field(None, min_length=1)
    in_stock: Optional[bool] = None

# ================== ROUTES ==================
@app.get("/products/", response_model=List[ProductResponse], tags=["products"])
def get_all_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Public: List products with pagination"""
    return db.query(models.Product).offset(skip).limit(limit).all()

@app.get("/products/{product_id}", response_model=ProductResponse, tags=["products"])
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Public: Get single product by ID"""
    product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/products/", response_model=ProductResponse, tags=["products"])
def create_product(
    product: ProductBase,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Create product"""
    db_product = models.Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/products/{product_id}", response_model=ProductResponse, tags=["products"])
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Update product (partial)"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")

    update_data = product_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_product, key, value)

    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["products"])
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Delete product"""
    db_product = db.query(models.Product).filter(models.Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
