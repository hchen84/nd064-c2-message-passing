import logging
import grpc
import service_pb2
import service_pb2_grpc
import logging

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

logging.basicConfig(
    handlers=[logging.StreamHandler()], format="%(asctime)s.%(msecs)03d [%(levelname)s] %(message)s", level=logging.INFO,  datefmt="%Y-%m-%d %H:%M:%S")

logging.info("Sending sample payload...")

try:
    channel = grpc.insecure_channel("localhost:32000")
    logging.info("channel on localhost:32000")
    stub = service_pb2_grpc.PersonServiceStub(channel)
    logging.info("PersonServiceStub set ")
    # Update this with desired payload
    order = service_pb2.PersonMessage(
        id=10001,
        first_name="foo",
        last_name='chen',
        company_name='mercedes'
    )
    logging.info("creat person message")
    response = stub.Create(order)
    logging.info(format(response))

except Exception as e:
    print(e)
    logging.error("Unable to send person msg")

try:
    channel = grpc.insecure_channel("localhost:32001")
    logging.info("channel on localhost:32001")
    stub = service_pb2_grpc.LocationServiceStub(channel)

    logging.info("LocationServiceStub set ")
    # Update this with desired payload
    order = service_pb2.LocationMessage(
        id=10001,
        person_id=1,
        longitude='9.0',
        latitude='48.0',
        creation_time="2022-06-08T10:37:06"
    )
    logging.info("creat lcoation message")
    response = stub.Create(order)
    logging.info(format(response))

except Exception as e:
    print(e)
    logging.error("Unable to send location msg")
