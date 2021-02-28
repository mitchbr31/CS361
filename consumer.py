import pika
import threading
import json
import base64
import time
"""
connection = pika.BlockingConnection(
    pika.ConnectionParameters(host='localhost', port=5672)
)

channel = connection.channel()

def callback(channel, method, properties, body):
    msg = json.loads(body)
    print("Received %r" % msg)
    if msg == "request":
        channel.basic_publish(exchange='', routing_key='hello', body=json.dumps('response'), \
         properties=pika.BasicProperties(delivery_mode=2,
    ))

channel.basic_consume(
    queue="hello", on_message_callback=callback, auto_ack=True
)

print("Waiting for messages, to exit press ctrl+C")
channel.start_consuming()
"""
class PikaMessenger():

    exchange_name = 'exchange'

    def __init__(self, *args, **kwargs):
        self.conn = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
        self.channel = self.conn.channel()
        self.channel.exchange_declare(
            exchange=self.exchange_name, 
            exchange_type='topic')

    def consume(self, keys, callback):
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        for key in keys:
            self.channel.queue_bind(
                exchange=self.exchange_name, 
                queue=queue_name, 
                routing_key=key)

        self.channel.basic_consume(
            queue=queue_name, 
            on_message_callback=callback, 
            auto_ack=True)

        self.channel.start_consuming()
    
    def stop_consume(self, keys):
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        for key in keys:
            self.channel.queue_bind(
                exchange=self.exchange_name, 
                queue=queue_name, 
                routing_key=key)
        self.channel.stop_consuming()  

    def publish(self, keys, callback, body):
        result = self.channel.queue_declare('', exclusive=True)
        queue_name = result.method.queue
        for key in keys:
            self.channel.queue_bind(
                exchange=self.exchange_name,
                queue=queue_name,
                routing_key=key
            )
        
        self.channel.basic_publish(exchange=self.exchange_name, routing_key='response', body=body, properties=pika.BasicProperties(delivery_mode=2,))


    def __enter__(self):
        return self


    def __exit__(self, exc_type, exc_value, traceback):
        self.conn.close()

def start_publisher():

    def callback(ch, method, properties, body):
        print(" [x] %r:%r published" % (method.routing_key, body))

    with PikaMessenger() as publisher:
        publisher.publish(keys=['response'], callback=callback, body=json.dumps("response body"))

def start_consumer():

    def callback(ch, method, properties, body):
        print(" [x] %r:%r consumed" % (method.routing_key, body))
        if body:
            consumer.stop_consume(keys=['request'])
            time.sleep(1)
            publisher_thread = threading.Thread(target=start_publisher)
            publisher_thread.start()

    with PikaMessenger() as consumer:
        consumer.consume(keys=['request'], callback=callback)




consumer_thread = threading.Thread(target=start_consumer)
consumer_thread.start()

publisher_thread = threading.Thread(target=start_publisher)
publisher_thread.start()