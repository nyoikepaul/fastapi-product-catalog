from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app.crud import product as crud_product
from app.schemas import product as schema_product
from app.db.session import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/", response_model=List[schema_product.Product])
def read_products(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return crud_product.get_products(db, skip=skip, limit=limit)

@router.post("/", response_model=schema_product.Product, status_code=status.HTTP_201_CREATED)
def create_product(product: schema_product.ProductCreate, db: Session = Depends(get_db)):
    return crud_product.create_product(db=db, product=product)
