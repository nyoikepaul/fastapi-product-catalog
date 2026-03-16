from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sys
import os

sys.path.append(os.path.dirname(os.path.realpath(__file__)))

from app.main import app as api_app

app = FastAPI(title="Expert Product Catalog")

# Serve expert frontend
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# Include all your existing API routes
app.include_router(api_app.router)

@app.get("/health")
def health():
    return {"status": "live", "database": "Supabase connected"}
