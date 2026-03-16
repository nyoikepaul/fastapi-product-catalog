from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

from app.routers.products import router as products_router
from app.routers.categories import router as categories_router
from app.core.database import init_db

app = FastAPI(title="Expert Product Catalog", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expert Frontend at root
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def serve_frontend():
    return FileResponse("static/index.html")

# API routes
app.include_router(products_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "healthy", "db": "Supabase"}

# Create tables on Supabase
@app.on_event("startup")
def startup():
    init_db()
