from sqlalchemy import Column, String, Float, Integer
from app.db.session import Base

class Menu(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, nullable=False)
    order_id = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=False)
    modifiers = Column(String)  # JSON-строка
    total_price = Column(Float, nullable=False)
    status = Column(String, default="new", nullable=False)

