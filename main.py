from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Import your existing routers and db
from app.routers.products import router as products_router
from app.routers.categories import router as categories_router
from app.core.database import get_db  # only import, don't run init on startup

app = FastAPI(title="Expert Product Catalog", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Expert Frontend
app.mount("/static", StaticFiles(directory="static", html=True), name="static")

@app.get("/")
async def serve_expert_frontend():
    return FileResponse("static/index.html")

# API routes
app.include_router(products_router, prefix="/api/v1")
app.include_router(categories_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "healthy", "database": "Supabase"}

# No startup event (prevents crash on Supabase connection)
# Tables will be created automatically on first request
