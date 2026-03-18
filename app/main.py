from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import text
import os
from app.db.session import get_db

app = FastAPI()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

def verify_key(key: str = Security(api_key_header)):
    if key != os.getenv("CATALOG_API_KEY"):
        raise HTTPException(status_code=403, detail="UNAUTHORIZED")
    return key

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT * FROM products ORDER BY id DESC"))
    return [dict(row._mapping) for row in result]

@app.put("/products/{p_id}", dependencies=[Depends(verify_key)])
def update_product(p_id: int, p: dict, db: Session = Depends(get_db)):
    try:
        db.execute(
            text("""UPDATE products SET 
                 name=:name, description=:desc, price=:price, 
                 stock=:stock, image_url=:img 
                 WHERE id=:id"""),
            {
                "name": p.get("name"), "desc": p.get("description"), 
                "price": p.get("price"), "stock": p.get("stock", 0),
                "img": p.get("image_url"), "id": p_id
            }
        )
        db.commit()
        return {"status": "SUCCESS"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))

# Keep your existing POST and DELETE routes below...
