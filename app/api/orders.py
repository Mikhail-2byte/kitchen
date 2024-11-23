from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.orders import OrderCreate, OrderStatusUpdate
from app.db.models import Order
from app.db.session import get_db
from app.rabbitmq.publisher import publish_to_broker
import json

router = APIRouter()

@router.post("/", response_model=dict)
async def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    existing_order = db.query(Order).filter(Order.order_id == order.order_id).first()
    if existing_order:
        raise HTTPException(status_code=400, detail="Order ID already exists")

    db_order = Order(
        order_id=order.order_id,
        items=json.dumps(order.items),
        total_price=order.total_price,
    )
    db.add(db_order)
    db.commit()
    db.refresh(db_order)

    await publish_to_broker({
        "order_id": order.order_id,
        "status": db_order.status,
        "total_price": order.total_price,
        "items": order.items,
    })

    return {"status": "Order created", "order": {"order_id": order.order_id, "status": db_order.status}}

@router.put("/{order_id}/status", response_model=dict)
async def update_order_status(order_id: str, status_update: OrderStatusUpdate, db: Session = Depends(get_db)):
    order = db.query(Order).filter(Order.order_id == order_id).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    order.status = status_update.status
    db.commit()

    await publish_to_broker({"order_id": order.order_id, "status": order.status})

    return {"status": "Order status updated", "order": {"order_id": order.order_id, "status": order.status}}
