from fastapi import APIRouter, Query
from typing import Optional
from app.db import db
from app.models import ProductModel
from bson import ObjectId
import re

router = APIRouter()
products_collection = db["products"]

# --- Create Product API ---
@router.post("/products", status_code=201)
def create_product(product: ProductModel):
    """
    Create a new product with sizes and quantities.
    """
    product_data = product.dict()
    result = products_collection.insert_one(product_data)
    product_data["_id"] = str(result.inserted_id)
    return product_data

# --- List Products API ---
@router.get("/products", status_code=200)
def list_products(
    name: Optional[str] = None,
    size: Optional[str] = None,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0)
):
    """
    List products with pagination and filtering.
    Returns only id, name, price (not sizes).
    """
    query = {}
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}
    if size:
        query["sizes.size"] = size

    cursor = products_collection.find(query).skip(offset).limit(limit)

    data = []
    for product in cursor:
        data.append({
            "id": str(product["_id"]),
            "name": product.get("name", ""),
            "price": product.get("price", 0.0)
        })

    # Pagination info
    page = {
        "next": str(offset + limit),
        "limit": limit,
        "previous": max(offset - limit, 0)
    }

    return {
        "data": data,
        "page": page
    }
