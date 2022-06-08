FROM python:3.8
LABEL maintainer="Chen"

COPY ./modules/kafka_consumer /kafka_consumer
WORKDIR /kafka_consumer

RUN pip install -r requirements.txt

EXPOSE 9092
CMD ["python", "-u", "consumer.py"]