from kafka import KafkaConsumer
import logging


def process_topic_loaction(msg):
    print("location:", msg)
    logging.info(msg.decode())


def process_topic_person(msg):
    print("person:", msg)
    logging.info(msg.decode())


def serve():
    logging.basicConfig(
        handlers=[logging.StreamHandler()], format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s", level=logging.INFO,  datefmt="%Y-%m-%d %H:%M:%S")
    # KAFKA_SERVER = 'localhost:30005'
    KAFKA_SERVER = 'kafka-headless:9092'

    # consumer = KafkaConsumer()
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER)
    consumer.subscribe(['location', 'person'])
    logging.info("start KafkaConsumer")

    func_dict = {"location": process_topic_loaction,
                 "person": process_topic_person}

    while True:
        msg = consumer.poll(1.0)

        if msg is None or len(msg) == 0:
            continue

        for tp, messages in msg.items():
            for message in messages:
                func_dict[tp.topic](message.value)


if __name__ == '__main__':
    serve()
