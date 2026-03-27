from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Use a persistent path that works on Vercel
DATABASE_URL = "sqlite:///./products.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock_quantity = Column(Integer, default=0)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int

def get_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != "super-secret-key-2026-pro":
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")
    return x_api_key

app = FastAPI(title="Product Catalog")

# Mount static files (your index.html)
app.mount("/static", StaticFiles(directory="static"), name="static")

# ============== AUTO SEED PRODUCTS ON STARTUP ==============
def seed_products():
    db: Session = SessionLocal()
    if db.query(Product).count() == 0:
        sample_products = [
            {"name": "Mechanical Keyboard", "description": "RGB backlit mechanical keyboard", "price": 8900, "stock_quantity": 5},
            {"name": "Wireless Earbuds Pro", "description": "Noise cancelling true wireless earbuds", "price": 4500, "stock_quantity": 12},
            {"name": "Laptop Stand Aluminium", "description": "Adjustable ergonomic laptop stand", "price": 2100, "stock_quantity": 8},
            {"name": "USB-C Hub 7-in-1", "description": "Multiport USB-C adapter", "price": 3200, "stock_quantity": 20},
            {"name": "Webcam 4K", "description": "Ultra HD streaming webcam", "price": 6700, "stock_quantity": 0},
            {"name": "Mouse Pad XL", "description": "Extended gaming mouse pad", "price": 1200, "stock_quantity": 15},
            {"name": "SSD 1TB NVMe", "description": "High-speed NVMe solid state drive", "price": 8500, "stock_quantity": 7},
            {"name": "27 inch 4K Monitor", "description": "IPS 4K display", "price": 28500, "stock_quantity": 3},
        ]
        for p in sample_products:
            db.add(Product(**p))
        db.commit()
        print("✅ Seeded 8 sample products successfully")
    db.close()

seed_products()

# Serve frontend
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# API Routes
@app.get("/api/v1/products", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.post("/api/v1/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/api/v1/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.model_dump(exclude_unset=True).items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/v1/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), api_key: str = Depends(get_api_key)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}

@app.get("/health")
def health():
    return {"status": "ok"}
