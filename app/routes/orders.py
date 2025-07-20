from fastapi import APIRouter
from app.models import OrderModel
from app.db import db
from bson import ObjectId

router = APIRouter()

@router.post("/orders", status_code=201)
def create_order(order: OrderModel):
    # Convert product IDs to ObjectId
    order_dict = order.dict()
    order_dict["products"] = [ObjectId(pid) for pid in order.products]
    result = db.orders.insert_one(order_dict)
    order_dict["_id"] = str(result.inserted_id)
    order_dict["products"] = [str(pid) for pid in order_dict["products"]]
    return order_dict

@router.get("/getorders/{user_id}", status_code=200)
def list_orders(user_id: str, limit: int = 10, offset: int = 0):
    orders = list(db.orders.find({"user_id": user_id}).skip(offset).limit(limit))
    for order in orders:
        order["_id"] = str(order["_id"])
        order["products"] = [str(pid) for pid in order["products"]]
    return orders
