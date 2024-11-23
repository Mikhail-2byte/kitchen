import json
from aiokafka import AIOKafkaProducer
from app.core.config import KAFKA_BROKER

producer = None

async def get_kafka_producer():
    global producer
    if producer is None:
        producer = AIOKafkaProducer(bootstrap_servers=KAFKA_BROKER)
        await producer.start()
    return producer

async def publish_to_kafka(topic: str, message: dict):
    kafka_producer = await get_kafka_producer()
    await kafka_producer.send_and_wait(topic, json.dumps(message).encode("utf-8"))
