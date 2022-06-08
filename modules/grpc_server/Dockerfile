FROM python:3.8
LABEL maintainer="Chen"

COPY ./modules/grpc_server /grpc_server
WORKDIR /grpc_server
RUN pip install -r requirements.txt

EXPOSE 5005
# command to run on container start
# RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ service.proto
# CMD ["python", "-m", "grpc_tools.protoc", "-I./", "--python_out=./",  "--grpc_python_out=./", "service.proto"]

CMD [ "python", "-u", "server.py" ]