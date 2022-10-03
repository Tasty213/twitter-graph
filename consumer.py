from kafka import KafkaConsumer


def main():
    consumer = KafkaConsumer("twitter-users")
    for message in consumer:
        print(message)


if __name__ == "__main__":
    main()
