from fastapi import APIRouter, Depends, HTTPException, Query, Response, status
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.schemas.product import ProductBase, ProductResponse, ProductUpdate
from app.crud.product import (
    get_products,
    get_product_by_id,
    create_product_in_db,
    update_product_in_db,
    delete_product_in_db,
)
from app.core.security import get_api_key

router = APIRouter(prefix="/products", tags=["products"])

@router.get("/", response_model=List[ProductResponse])
def get_all_products(
    db: Session = Depends(get_db),
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)
):
    """Public: List products with pagination"""
    return get_products(db, skip, limit)

@router.get("/{product_id}", response_model=ProductResponse)
def get_product(product_id: int, db: Session = Depends(get_db)):
    """Public: Get single product"""
    product = get_product_by_id(db, product_id)
    if product is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.post("/", response_model=ProductResponse)
def create_product(
    product: ProductBase,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Create product"""
    return create_product_in_db(db, product)

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(
    product_id: int,
    product_update: ProductUpdate,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Partial update"""
    updated = update_product_in_db(db, product_id, product_update)
    if updated is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return updated

@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
    product_id: int,
    db: Session = Depends(get_db),
    api_key: str = Depends(get_api_key)
):
    """Protected: Delete product"""
    deleted = delete_product_in_db(db, product_id)
    if deleted is None:
        raise HTTPException(status_code=404, detail="Product not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
