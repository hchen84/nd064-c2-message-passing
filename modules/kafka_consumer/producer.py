from kafka import KafkaProducer

try:
    KAFKA_SERVER = 'localhost:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)
except:
    KAFKA_SERVER = 'kafka-headless:9092'
    producer = KafkaProducer(bootstrap_servers=KAFKA_SERVER)


TOPIC_NAME = 'location'
producer.send(TOPIC_NAME, b'Test Message!!!')
producer.flush()


TOPIC_NAME = 'person'
producer.send(TOPIC_NAME, b'Test Message2!!!')
producer.flush()
