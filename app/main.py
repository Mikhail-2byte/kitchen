from fastapi import FastAPI
from app.api import orders
from app.db.session import Base, engine

app = FastAPI(title="Order Service")

# Создаем таблицы, если их нет
Base.metadata.create_all(bind=engine)

# Регистрируем маршруты
app.include_router(orders.router, prefix="/orders", tags=["Orders"])

@app.on_event("startup")
async def startup_event():
    print("Starting application...")

@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down application...")
