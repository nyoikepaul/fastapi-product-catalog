from fastapi import FastAPI, Depends, HTTPException, Security, Query
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from app.db.session import get_db

app = FastAPI(title="SYSTEM_CATALOG_PROD")

API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def verify_api_key(api_key_header: str = Security(api_key_header)):
    expected = os.getenv("CATALOG_API_KEY")
    if not expected or api_key_header != expected:
        raise HTTPException(status_code=403, detail="INVALID_CREDENTIALS")
    return api_key_header

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    # Fetching all columns to ensure UI cards have data
    result = db.execute(text("SELECT id, name, description, price, category, image_url FROM products ORDER BY id DESC"))
    return [dict(row._mapping) for row in result]

@app.post("/products/", dependencies=[Depends(verify_api_key)])
def create_product(product: dict, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO products (name, description, price, category, image_url) VALUES (:name, :description, :price, :category, :image_url)"),
        {
            "name": product.get("name"), 
            "description": product.get("description"), 
            "price": product.get("price"),
            "category": product.get("category", "General"),
            "image_url": product.get("image_url")
        }
    )
    db.commit()
    return {"status": "SUCCESS"}

@app.delete("/products/{product_id}", dependencies=[Depends(verify_api_key)])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db.execute(text("DELETE FROM products WHERE id=:id"), {"id": product_id})
    db.commit()
    return {"status": "DELETED"}
