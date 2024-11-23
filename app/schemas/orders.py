from pydantic import BaseModel

class OrderCreate(BaseModel):
    order_id: str
    items: list[dict]
    total_price: float

class OrderStatusUpdate(BaseModel):
    status: str
