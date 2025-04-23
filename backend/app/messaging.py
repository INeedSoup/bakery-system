# backend/app/messaging.py

import os, json
import pika

RABBIT_HOST = os.getenv("RABBIT_HOST", "rabbitmq")
RABBIT_USER = os.getenv("RABBIT_USER", "guest")
RABBIT_PASS = os.getenv("RABBIT_PASS", "guest")
QUEUE_NAME = "orders"

def publish_order_message(order):
    """Publish order details to the 'orders' queue."""
    creds = pika.PlainCredentials(RABBIT_USER, RABBIT_PASS)
    params = pika.ConnectionParameters(host=RABBIT_HOST, credentials=creds)
    connection = pika.BlockingConnection(params)
    channel = connection.channel()
    channel.queue_declare(queue=QUEUE_NAME, durable=True)
    message = json.dumps({
        "order_id":    order.id,
        "product_id":  order.product_id,
        "quantity":    order.quantity,
        "status":      order.status.value,
        "created_at":  order.created_at.isoformat()
    })
    channel.basic_publish(
        exchange="",
        routing_key=QUEUE_NAME,
        body=message,
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()
