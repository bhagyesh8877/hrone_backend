from pydantic import BaseModel
from typing import List, Optional

# --- Product Models ---
class SizeEntry(BaseModel):
    size: str
    quantity: int

class ProductModel(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    sizes: List[SizeEntry]

class ProductOut(ProductModel):
    _id: str

# --- Order Models ---
class OrderItem(BaseModel):
    productId: str
    qty: int

class OrderModel(BaseModel):
    userId: str
    items: List[OrderItem]

class OrderOut(BaseModel):
    id: str
    items: List[dict]
