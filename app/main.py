from fastapi import FastAPI
from app.api.endpoints import products
from app.core.config import settings
from app.db.session import engine, Base

# Create the database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.PROJECT_NAME)

app.include_router(products.router, prefix="/products", tags=["products"])

@app.get("/")
async def root():
    return {"message": "Welcome to the Expert Level Product Catalog API"}
