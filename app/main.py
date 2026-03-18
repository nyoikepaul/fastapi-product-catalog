from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from app.db.session import get_db

app = FastAPI()

@app.get("/products/")
def read_products(
    q: str = Query(None), 
    min_price: float = Query(0), 
    max_price: float = Query(999999),
    db: Session = Depends(get_db)
):
    try:
        # Base query supporting the UI filters
        sql = "SELECT id, name, description, price, category FROM products WHERE price >= :min AND price <= :max"
        params = {"min": min_price, "max": max_price}

        if q:
            sql += " AND (name ILIKE :q OR description ILIKE :q)"
            params["q"] = f"%{q}%"
        
        sql += " ORDER BY id DESC"
        
        result = db.execute(text(sql), params)
        products = [dict(row._mapping) for row in result]
        
        # Log for Vercel debugging
        print(f"DEBUG: Found {len(products)} products")
        return products
    except Exception as e:
        print(f"CRITICAL_ERR: {str(e)}")
        raise HTTPException(status_code=500, detail="DB_HANDSHAKE_FAILED")

@app.get("/health")
def health_check():
    return {"status": "operational", "node": "NBO_SECURE_01"}
