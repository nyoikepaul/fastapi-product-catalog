from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional
import os
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, Session, declarative_base

# Vercel-safe SQLite (persists in /tmp during testing)
DATABASE_URL = "sqlite:////tmp/products.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    description = Column(String, nullable=True)
    price = Column(Float)
    stock_quantity = Column(Integer)

Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic models (matches your frontend exactly)
class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int

class ProductResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int

# API Key protection (use this exact key in sidebar for now)
def get_api_key(x_api_key: str = Header(None)):
    expected = os.getenv("X_API_KEY", "demo-key-12345")
    if not x_api_key or x_api_key != expected:
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")
    return x_api_key

app = FastAPI(title="Expert Product Catalog", version="2.0")

# Serve your expert frontend
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def serve_expert_frontend():
    return FileResponse("static/index.html")

# API routes (exactly what your JS calls)
@app.get("/api/v1/products", response_model=List[ProductResponse])
def list_products(db: Session = Depends(get_db)):
    return db.query(Product).all()

@app.get("/api/v1/products/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    product = db.query(Product).filter(Product.id == product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@app.post("/api/v1/products", response_model=ProductResponse)
def create_product(product: ProductCreate, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    db_product = Product(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.put("/api/v1/products/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product: ProductCreate, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product

@app.delete("/api/v1/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    db_product = db.query(Product).filter(Product.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return {"detail": "Product deleted"}

@app.get("/health")
def health():
    return {"status": "healthy", "db": "SQLite (ready for Supabase)"}
