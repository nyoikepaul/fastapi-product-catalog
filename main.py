from fastapi import FastAPI, Header, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI(title="Product Catalog API")

# 1. Mount static folder for the frontend
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def serve_frontend():
    """Serves the CRUD frontend on the root URL"""
    return FileResponse("static/index.html")

# --- Models ---
class Product(BaseModel):
    id: Optional[int] = None
    name: str
    description: Optional[str] = None
    price: float

# --- Mock Database (Replace with your SQLAlchemy DB logic) ---
db = [
    {"id": 1, "name": "Mechanical Keyboard", "description": "Clicky switches", "price": 85.00},
    {"id": 2, "name": "Wireless Mouse", "description": "Ergonomic design", "price": 45.99}
]
current_id = 2

# --- Simple Auth ---
# In production, use environment variables (e.g., os.getenv("API_KEY"))
VALID_API_KEY = "mysecretkey" 

def verify_api_key(x_api_key: str):
    if x_api_key != VALID_API_KEY:
        raise HTTPException(status_code=401, detail="Invalid or missing API Key")

# --- CRUD Endpoints ---

@app.get("/products", response_model=List[Product])
async def get_products():
    return db

@app.post("/products", response_model=Product)
async def create_product(product: Product, x_api_key: str = Header(None)):
    verify_api_key(x_api_key)
    global current_id
    current_id += 1
    new_product = product.dict()
    new_product["id"] = current_id
    db.append(new_product)
    return new_product

@app.put("/products/{product_id}", response_model=Product)
async def update_product(product_id: int, product: Product, x_api_key: str = Header(None)):
    verify_api_key(x_api_key)
    for index, p in enumerate(db):
        if p["id"] == product_id:
            updated_product = product.dict()
            updated_product["id"] = product_id
            db[index] = updated_product
            return updated_product
    raise HTTPException(status_code=404, detail="Product not found")

@app.delete("/products/{product_id}")
async def delete_product(product_id: int, x_api_key: str = Header(None)):
    verify_api_key(x_api_key)
    for index, p in enumerate(db):
        if p["id"] == product_id:
            del db[index]
            return {"message": "Product deleted"}
    raise HTTPException(status_code=404, detail="Product not found")

