from kafka import KafkaConsumer
import logging
import json
from app.udaconnect.services import ConnectionService, LocationService, PersonService
from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)


def process_topic_location(msg):
    try:
        print("location:", msg)
        # logging.info(msg.decode())
        new_location: Location = LocationService.create(
            json.loads(msg.decode()))
        logging.info("create new location")
    except:
        logging.error("can't creat location for " + json.loads(msg.decode()))


def process_topic_person(msg):
    try:
        print("person:", msg)
        # logging.info(msg.decode())
        new_person: Person = PersonService.create(json.loads(msg.decode()))
        logging.info("create new person")
    except:
        logging.error("can't creat person for " + json.loads(msg.decode()))


def serve():
    logging.basicConfig(
        handlers=[logging.StreamHandler()], format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s", level=logging.INFO,  datefmt="%Y-%m-%d %H:%M:%S")
    # KAFKA_SERVER = 'localhost:30005'
    KAFKA_SERVER = 'kafka-headless:9092'

    logging.info("starting KafkaConsumer")
    # consumer = KafkaConsumer()
    consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER)
    consumer.subscribe(['location', 'person'])
    logging.info("subscribe topic: location and person")

    func_dict = {"location": process_topic_location,
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
