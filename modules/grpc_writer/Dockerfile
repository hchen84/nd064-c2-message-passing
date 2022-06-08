FROM python:3.8
LABEL maintainer="Chen"

COPY ./modules/grpc_writer /grpc_writer
WORKDIR /grpc_writer
RUN pip install -r requirements.txt

EXPOSE 5005
# command to run on container start
# RUN python -m grpc_tools.protoc -I./ --python_out=./ --grpc_python_out=./ service.proto
# CMD ["python", "-m", "grpc_tools.protoc", "-I./", "--python_out=./",  "--grpc_python_out=./", "service.proto"]

CMD [ "python", "-u", "writer.py" ]