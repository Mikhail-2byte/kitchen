import asyncio
from aiokafka import AIOKafkaConsumer
from app.core.config import KAFKA_BROKER

async def consume_from_kafka(topic: str):
    consumer = AIOKafkaConsumer(
        topic,
        bootstrap_servers=KAFKA_BROKER,
        group_id="order_status_group",
        auto_offset_reset="earliest",
    )
    await consumer.start()
    try:
        async for message in consumer:
            print(f"Consumed message: {message.value.decode('utf-8')}")
            # Здесь можно обработать сообщение (например, обновить статус заказа)
    finally:
        await consumer.stop()

# Пример запуска
if __name__ == "__main__":
    asyncio.run(consume_from_kafka("order_status"))
