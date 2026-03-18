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

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return """
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>CATALOG // SYSTEM</title>
        <script src="https://cdn.tailwindcss.com"></script>
        <style>
            body { background: #0d1117; color: #c9d1d9; font-family: ui-monospace, monospace; }
            .card { background: #161b22; border: 1px solid #30363d; }
            .input-field { background: #0d1117; border: 1px solid #30363d; color: white; padding: 8px; border-radius: 4px; }
            .btn-primary { background: #238636; color: white; padding: 8px 16px; border-radius: 6px; font-weight: bold; }
            .btn-primary:hover { background: #2ea043; }
            #modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.8); align-items: center; justify-content: center; z-index: 50; }
        </style>
    </head>
    <body class="p-4 md:p-10">
        <header class="max-w-4xl mx-auto mb-10 flex justify-between items-center border-b border-gray-800 pb-6">
            <div>
                <h1 class="text-2xl font-bold text-blue-400 tracking-tighter">SYSTEM.CATALOG</h1>
                <p class="text-[10px] text-gray-500 mt-1 uppercase tracking-widest">NBO_SECURE_NODE_01</p>
            </div>
            <div class="flex gap-3">
                <input type="password" id="api-key-input" placeholder="Enter API Key" class="input-field text-xs w-32">
                <button onclick="document.getElementById('modal').style.display='flex'" class="btn-primary text-xs">+ NEW_ENTRY</button>
            </div>
        </header>

        <div id="catalog" class="max-w-4xl mx-auto grid grid-cols-1 md:grid-cols-2 gap-4">
            <div class="text-gray-600 animate-pulse">SYNCHRONIZING_DATABASE...</div>
        </div>

        <div id="modal">
            <div class="card p-8 rounded-lg w-full max-w-md">
                <h2 class="text-lg font-bold mb-6 text-blue-400 underline">INITIALIZE_NEW_RECORD</h2>
                <div class="flex flex-col gap-4">
                    <input id="p-name" placeholder="Product Name" class="input-field">
                    <textarea id="p-desc" placeholder="System Description" class="input-field h-24"></textarea>
                    <input id="p-price" type="number" placeholder="Price (USD)" class="input-field">
                    <div class="flex gap-3 mt-4">
                        <button onclick="saveProduct()" class="btn-primary flex-1">COMMIT_TO_DB</button>
                        <button onclick="document.getElementById('modal').style.display='none'" class="bg-gray-800 px-4 py-2 rounded text-xs">ABORT</button>
                    </div>
                </div>
            </div>
        </div>

        <script>
            async function fetchCatalog() {
                const res = await fetch('/products/');
                const data = await res.json();
                document.getElementById('catalog').innerHTML = data.map(item => `
                    <div class="card p-6 rounded-lg">
                        <div class="text-[9px] text-blue-500 mb-1">REF: ${item.id}</div>
                        <h3 class="text-lg font-bold text-white">${item.name}</h3>
                        <p class="text-xs text-gray-400 mt-2 mb-4">${item.description || ''}</p>
                        <div class="flex justify-between items-end pt-4 border-t border-gray-800">
                            <span class="text-green-400 font-bold">$${item.price}</span>
                            <span class="text-[9px] text-gray-600 uppercase">Status: Verified</span>
                        </div>
                    </div>
                `).join('');
            }

            async function saveProduct() {
                const apiKey = document.getElementById('api-key-input').value;
                const payload = {
                    name: document.getElementById('p-name').value,
                    description: document.getElementById('p-desc').value,
                    price: parseFloat(document.getElementById('').value)
                };

                const res = await fetch('/products/', {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json', 'X-API-Key': apiKey },
                    body: JSON.stringify(payload)
                });

                if (res.ok) {
                    document.getElementById('modal').style.display = 'none';
                    fetchCatalog();
                } else {
                    alert("ERROR: ACCESS_DENIED. Check API Key.");
                }
            }
            fetchCatalog();
        </script>
    </body>
    </html>
    """

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, name, description, price FROM products ORDER BY id DESC"))
    return [dict(row._mapping) for row in result]

@app.post("/products/", dependencies=[Depends(verify_api_key)])
def create_product(product: dict, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO products (name, description, price) VALUES (:name, :description, :price)"),
        {"name": product.get("name"), "description": product.get("description"), "price": product.get("price")}
    )
    db.commit()
    return {"status": "SUCCESS"}
