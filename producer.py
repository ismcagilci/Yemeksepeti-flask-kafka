import time
from kafka import KafkaProducer

import json

producer = KafkaProducer(
    value_serializer = lambda m : json.dumps(m).encode('utf-8'),bootstrap_servers=['localhost:9092'])

def send_kafka(data):
    try:
        print("{} is sending to Kafka".format(data))
        producer.send("yemeksepeti-kafka", value=data)
    except Exception as e:
        print(e)
