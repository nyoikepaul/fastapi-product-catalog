from fastapi import APIRouter, Depends, HTTPException, status, Security
from fastapi.security.api_key import APIKeyHeader
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import List
from uuid import UUID

from app.db.session import get_db
from app.models.product import Product
from app.schemas.product import ProductCreate, ProductResponse
from app.core.config import settings

router = APIRouter()
api_key_header = APIKeyHeader(name="X-API-Key", auto_error=True)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key != settings.API_KEY_SECRET:
        raise HTTPException(status_code=403, detail="Invalid API Key")
    return api_key

@router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(
    product_in: ProductCreate, 
    db: AsyncSession = Depends(get_db),
    _ = Depends(get_api_key)
):
    obj = Product(**product_in.model_dump())
    db.add(obj)
    await db.commit()
    await db.refresh(obj)
    return obj

@router.get("/", response_model=List[ProductResponse])
async def list_products(db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Product))
    return result.scalars().all()
