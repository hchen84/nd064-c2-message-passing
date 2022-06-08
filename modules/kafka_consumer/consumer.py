from kafka import KafkaConsumer
import logging
import json
from geoalchemy2.functions import ST_AsText, ST_Point
import psycopg2
import os

from shapely.geometry.point import Point
from geoalchemy2.shape import from_shape


DB_USERNAME = os.environ["DB_USERNAME"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_HOST = os.environ["DB_HOST"]
DB_PORT = os.environ["DB_PORT"]
DB_NAME = os.environ["DB_NAME"]

conn = psycopg2.connect(
    host=DB_HOST,
    database=DB_NAME,
    user=DB_USERNAME,
    password=DB_PASSWORD,
    port=DB_PORT)


def process_topic_location(msg):
    try:
        print("location:", msg)
        data = json.loads(msg.decode())

        wkb_element = from_shape(
            Point(float(data["latitude"]), float(data["longitude"])))

        sql_txt = "insert into public.location (id, person_id, coordinate, creation_time) values ({}, {}, '{}', '{}')".format(
            data["id"], data["person_id"], wkb_element.desc, data["creation_time"])
        cur = conn.cursor()
        cur.execute(sql_txt)
        conn.commit()

        logging.info("create new location")
    except Exception as e:
        print(e)
        logging.error("can't create location for " + msg.decode())


def process_topic_person(msg):
    try:
        print("person:", msg)
        # logging.info(msg.decode())
        # new_person: Person = PersonService.create(json.loads(msg.decode()))
        data = json.loads(msg.decode())
        sql_txt = "insert into public.person (id, first_name, last_name, company_name) values ({}, '{}', '{}', '{}')".format(
            data["id"], data["first_name"], data["last_name"], data["company_name"])
        cur = conn.cursor()
        cur.execute(sql_txt)
        conn.commit()

        logging.info("create new person")
    except Exception as e:
        print(e)
        logging.error("can't create person for " + msg.decode())


def serve():
    logging.basicConfig(
        handlers=[logging.StreamHandler()], format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s", level=logging.INFO,  datefmt="%Y-%m-%d %H:%M:%S")

    logging.info("starting KafkaConsumer")
    try:
        KAFKA_SERVER = 'localhost:30005'  # for local testing
        consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER)
    except:
        try:
            KAFKA_SERVER = 'kafka-headless:9092'  # for deployment
            consumer = KafkaConsumer(bootstrap_servers=KAFKA_SERVER)
        except Exception as e:
            print(e)
            logging.error("can't connect to bootstrap_servers")
            return

    try:
        consumer.subscribe(['location', 'person'])
        logging.info("subscribe topic: location and person")
    except Exception as e:
        print(e)
        logging.error("can't subscribe topic: location and person")

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
