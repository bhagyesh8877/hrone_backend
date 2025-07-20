from fastapi import APIRouter, HTTPException, Query
from typing import Dict
from app.db import db
from app.models import OrderModel
from bson import ObjectId

router = APIRouter()

orders_collection = db["orders"]
products_collection = db["products"]

# --- Create Order API ---
@router.post("/orders", status_code=201)
def create_order(order_data: Dict):
    """
    Create an order with userId and items (productId, qty).
    """
    try:
        user_id = order_data["userId"]
        items = order_data["items"]
    except KeyError:
        raise HTTPException(status_code=400, detail="Missing userId or items")

    parsed_items = []
    for item in items:
        if "productId" not in item or "qty" not in item:
            raise HTTPException(status_code=400, detail="Each item must include productId and qty")
        try:
            parsed_items.append({
                "productId": ObjectId(item["productId"]),
                "qty": item["qty"]
            })
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid productId format")

    order_doc = {
        "userId": user_id,
        "items": parsed_items
    }

    result = orders_collection.insert_one(order_doc)

    return {
        "id": str(result.inserted_id)
    }

# --- Get Orders API ---
@router.get("/orders", status_code=200)
def list_orders(limit: int = Query(10, ge=1), offset: int = Query(0, ge=0)):
    """
    Get list of orders with product details and pagination.
    """
    pipeline = [
        {"$skip": offset},
        {"$limit": limit},
        {"$unwind": "$items"},
        {
            "$lookup": {
                "from": "products",
                "localField": "items.productId",
                "foreignField": "_id",
                "as": "productDetails"
            }
        },
        {"$unwind": {"path": "$productDetails", "preserveNullAndEmptyArrays": True}},
        {
            "$group": {
                "_id": "$_id",
                "userId": {"$first": "$userId"},
                "items": {
                    "$push": {
                        "productDetails": {
                            "id": {"$toString": "$productDetails._id"},
                            "name": "$productDetails.name"
                        },
                        "qty": "$items.qty"
                    }
                }
            }
        }
    ]

    results = list(orders_collection.aggregate(pipeline))

    formatted_orders = []
    for order in results:
        formatted_orders.append({
            "id": str(order["_id"]),
            "items": order["items"]
        })

    page_info = {
        "next": str(offset + limit),
        "limit": limit,
        "previous": max(offset - limit, 0)
    }

    return {
        "data": formatted_orders,
        "page": page_info
    }
