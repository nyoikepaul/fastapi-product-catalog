from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.core.database import init_db
from app.routers.products import router as products_router
from app.routers.categories import router as categories_router

app = FastAPI(
    title="Expert Product Catalog API",
    description="Production-ready with Supabase",
    version="2.0.0"
)

# CORS + Static Frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def serve_expert_frontend():
    return FileResponse("static/index.html")

# All your existing API routes
app.include_router(products_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")

@app.get("/health")
def health_check():
    return {"status": "healthy", "database": "Supabase Live"}

# Startup: create tables on Supabase
@app.on_event("startup")
def startup_event():
    init_db()
