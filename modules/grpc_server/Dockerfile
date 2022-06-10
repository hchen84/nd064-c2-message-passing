FROM python:3.8
LABEL maintainer="Chen"

COPY ./modules/grpc_server /grpc_server
WORKDIR /grpc_server
RUN pip install -r requirements.txt

EXPOSE 5005

CMD [ "python", "-u", "server.py" ]