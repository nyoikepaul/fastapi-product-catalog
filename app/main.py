from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.responses import HTMLResponse
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.orm import Session
from sqlalchemy import text
import os

from app.db.session import get_db

app = FastAPI(title="Secure System Catalog")

# --- EXPERT LOGIC: SECURITY ---
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=True)

def verify_api_key(api_key_header: str = Security(api_key_header)):
    expected_key = os.getenv("CATALOG_API_KEY")
    if not expected_key or api_key_header != expected_key:
        raise HTTPException(status_code=403, detail="ERR: INVALID_OR_MISSING_CREDENTIALS")
    return api_key_header

# --- FRONTEND UI ---
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SYSTEM.CATALOG // PROD</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
    <style>
        body { font-family: 'JetBrains Mono', monospace; background-color: #090a0f; color: #c9d1d9; }
        .glass-panel { background: rgba(22, 27, 34, 0.6); border: 1px solid #30363d; backdrop-filter: blur(8px); }
        .glass-panel:hover { border-color: #58a6ff; box-shadow: 0 0 15px rgba(88, 166, 255, 0.1); }
        .glow-text { text-shadow: 0 0 8px rgba(88, 166, 255, 0.4); }
        .watermark { position: fixed; bottom: 10px; right: 10px; opacity: 0.15; font-size: 0.75rem; pointer-events: none; }
    </style>
</head>
<body class="p-4 md:p-8 antialiased min-h-screen flex flex-col">
    <div class="max-w-5xl mx-auto w-full flex-grow">
        <header class="mb-8 border-b border-gray-800 pb-4 flex flex-col md:flex-row md:justify-between md:items-end gap-2">
            <div>
                <h1 class="text-2xl md:text-3xl font-bold text-blue-400 glow-text">~/catalog/system_view</h1>
                <p class="text-[10px] md:text-xs text-green-500 mt-2 flex items-center gap-2">
                    <span class="relative flex h-2 w-2"><span class="animate-ping absolute inline-flex h-full w-full rounded-full bg-green-400 opacity-75"></span><span class="relative inline-flex rounded-full h-2 w-2 bg-green-500"></span></span>
                    STATUS: ONLINE | LATENCY: <span id="latency-metric">--</span>ms
                </p>
            </div>
            <div class="text-[10px] md:text-xs text-gray-500 text-left md:text-right font-mono">
                <p>NODE: NBO_SECURE_01</p>
                <p>ENV: PRODUCTION</p>
            </div>
        </header>
        <main id="product-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
            <div class="glass-panel p-5 rounded-sm animate-pulse flex flex-col gap-3 h-32">
                <div class="h-4 bg-gray-800 w-2/3 rounded"></div>
            </div>
        </main>
    </div>
    <div class="watermark tracking-widest">SYSTEM_INTEGRITY: VERIFIED // V.1.0.0</div>
    <script>
        const startTime = performance.now();
        async function loadCatalog() {
            const grid = document.getElementById('product-grid');
            try {
                const res = await fetch('/products/');
                const data = await res.json();
                document.getElementById('latency-metric').innerText = Math.round(performance.now() - startTime);
                grid.innerHTML = '';
                if (data.length === 0) {
                    grid.innerHTML = `<div class="col-span-full text-center text-gray-500 py-10 border border-dashed border-gray-700">NO_DATA: RUN_SEED_PROTOCOL</div>`;
                    return;
                }
                data.forEach(item => {
                    grid.innerHTML += `
                        <div class="glass-panel p-5 rounded-sm transition-all relative overflow-hidden flex flex-col justify-between group">
                            <div class="absolute top-0 right-0 bg-gray-800/50 text-gray-500 text-[9px] px-2 py-1 border-l border-b border-gray-700/50 font-mono">UID_${String(item.id).padStart(4, '0')}</div>
                            <div>
                                <h2 class="text-base font-bold text-gray-100 mb-2">${item.name}</h2>
                                <p class="text-xs text-gray-400 mb-4">${item.description || ''}</p>
                            </div>
                            <div class="flex justify-between items-end border-t border-gray-800/80 pt-3 mt-2">
                                <span class="text-green-400 font-bold font-mono">$${parseFloat(item.price).toFixed(2)}</span>
                                <span class="text-[10px] text-blue-400 opacity-0 group-hover:opacity-100 transition-opacity underline cursor-pointer">DETAILS_LOG</span>
                            </div>
                        </div>
                    `;
                });
            } catch (e) {
                grid.innerHTML = `<div class="text-red-500 font-mono">[FATAL]: DB_CONN_REFUSED</div>`;
            }
        }
        setTimeout(loadCatalog, 300);
    </script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return HTML_TEMPLATE

@app.get("/products/")
def read_products(db: Session = Depends(get_db)):
    result = db.execute(text("SELECT id, name, description, price FROM products"))
    return [dict(row._mapping) for row in result]

@app.post("/products/", dependencies=[Depends(verify_api_key)])
def create_product(product: dict, db: Session = Depends(get_db)):
    db.execute(
        text("INSERT INTO products (name, description, price) VALUES (:name, :description, :price)"),
        {"name": product.get("name"), "description": product.get("description"), "price": product.get("price")}
    )
    db.commit()
    return {"status": "success"}
