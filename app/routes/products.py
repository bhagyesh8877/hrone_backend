from fastapi import APIRouter, Query
from app.models import ProductModel
from app.db import db
from bson import ObjectId
import re

router = APIRouter()

# Use the "task" database's products collection
products_collection = db["products"]

@router.post("/products", status_code=201)
def create_product(product: ProductModel):
    """
    Create a new product in the products collection.
    Returns the created product with _id as string.
    """
    product_data = product.dict()
    result = products_collection.insert_one(product_data)
    
    product_data["_id"] = str(result.inserted_id)
    return product_data

@router.get("/listproducts", status_code=200)
def list_products(
    name: str = None, # type: ignore   
    size: str = None,  # type: ignore 
    limit: int = Query(10, ge=1),
    
    offset: int = Query(0, ge=0)
):
    """
    List products with optional filters (name, size),
    and support pagination using limit and offset.
    """
    query = {}
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}  # case-insensitive regex
    if size:
        query["size"] = size

    products = list(products_collection.find(query).skip(offset).limit(limit))
    
    # Convert ObjectId to string for each product
    for product in products:
        product["_id"] = str(product["_id"])

    return products
