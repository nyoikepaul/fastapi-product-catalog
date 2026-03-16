from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product import ProductResponse, ProductCreate, ProductUpdate
from app.crud.product import get_products, get_product, create_product, update_product, delete_product
from app.api.deps import get_db, get_api_key

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
def list_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100),
    category_id: Optional[int] = None,
    min_price: Optional[float] = None,
    search: Optional[str] = None,
):
    return get_products(db, skip, limit, category_id, min_price, search)

@router.get("/{product_id}", response_model=ProductResponse)
def read_product(product_id: int, db: Session = Depends(get_db)):
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_new_product(product: ProductCreate, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    return create_product(db, product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_existing(product_id: int, product: ProductUpdate, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    updated = update_product(db, product_id, product)
    if not updated:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=204)
def delete_existing(product_id: int, db: Session = Depends(get_db), api_key=Depends(get_api_key)):
    if not delete_product(db, product_id):
        raise HTTPException(status_code=404, detail="Product not found")
