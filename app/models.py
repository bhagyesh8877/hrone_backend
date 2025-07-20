from pydantic import BaseModel, Field
from typing import List, Optional

class ProductModel(BaseModel):
    name: str
    description: Optional[str]
    price: float
    size: Optional[str]

class ProductOut(ProductModel):
    _id: str

class OrderModel(BaseModel):
    user_id: str
    products: List[str]  # Product IDs as strings

class OrderOut(OrderModel):
    _id: str
