from kafka import KafkaConsumer


def get_consumer():
    consumer = KafkaConsumer(
        "yemeksepeti-kafka",
        bootstrap_servers=['localhost:9092'],
        auto_offset_reset="earliest",
        enable_auto_commit=False,
        consumer_timeout_ms=1000
    )
    return consumer


