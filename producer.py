import json

from kafka import KafkaProducer

if __name__ == "__main__":
    producer = KafkaProducer(value_serializer=lambda v: json.dumps(v).encode('utf-8'))
    message = producer.send("twitter-users", {"test": "test"})
    message.get(timeout=60)
    print("message sent")
