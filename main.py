from fastapi import FastAPI, Depends, HTTPException, Header
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Product Catalog")

# Mount your existing frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

# Sample products (in-memory - survives Vercel deploys)
PRODUCTS = [
    {"id": 1, "name": "Mechanical Keyboard", "description": "RGB backlit mechanical keyboard", "price": 8900, "stock_quantity": 5},
    {"id": 2, "name": "Wireless Earbuds Pro", "description": "Noise cancelling true wireless earbuds", "price": 4500, "stock_quantity": 12},
    {"id": 3, "name": "Laptop Stand Aluminium", "description": "Adjustable ergonomic laptop stand", "price": 2100, "stock_quantity": 8},
    {"id": 4, "name": "USB-C Hub 7-in-1", "description": "Multiport USB-C adapter", "price": 3200, "stock_quantity": 20},
    {"id": 5, "name": "Webcam 4K", "description": "Ultra HD streaming webcam", "price": 6700, "stock_quantity": 0},
    {"id": 6, "name": "Mouse Pad XL", "description": "Extended gaming mouse pad", "price": 1200, "stock_quantity": 15},
    {"id": 7, "name": "SSD 1TB NVMe", "description": "High-speed NVMe solid state drive", "price": 8500, "stock_quantity": 7},
    {"id": 8, "name": "27 inch 4K Monitor", "description": "IPS 4K display", "price": 28500, "stock_quantity": 3},
]

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0

def get_api_key(x_api_key: Optional[str] = Header(None)):
    if x_api_key != "super-secret-key-2026-pro":
        raise HTTPException(status_code=401, detail="Invalid X-API-Key")
    return x_api_key

# Serve frontend
@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# API Endpoints
@app.get("/api/v1/products")
def list_products():
    return PRODUCTS

@app.post("/api/v1/products")
def create_product(product: ProductCreate, api_key: str = Depends(get_api_key)):
    new_id = max(p["id"] for p in PRODUCTS) + 1 if PRODUCTS else 1
    new_product = {"id": new_id, **product.model_dump()}
    PRODUCTS.append(new_product)
    return new_product

@app.put("/api/v1/products/{product_id}")
def update_product(product_id: int, product: ProductCreate, api_key: str = Depends(get_api_key)):
    for p in PRODUCTS:
        if p["id"] == product_id:
            p.update(product.model_dump(exclude_unset=True))
            return p
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/api/v1/products/{product_id}")
def delete_product(product_id: int, api_key: str = Depends(get_api_key)):
    for i, p in enumerate(PRODUCTS):
        if p["id"] == product_id:
            del PRODUCTS[i]
            return {"detail": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")

@app.get("/health")
def health():
    return {"status": "ok", "products_count": len(PRODUCTS)}
