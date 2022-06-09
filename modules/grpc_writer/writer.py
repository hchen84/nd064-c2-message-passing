import logging
import grpc
import service_pb2
import service_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

try:
    channel = grpc.insecure_channel("10.43.254.112:grpc")
    logging.info("10.43.254.112:grpc")
except:
    channel = grpc.insecure_channel("localhost:grpc")
    logging.info("localhost:grpc")
print("channel set ")
stub = service_pb2_grpc.LocationServiceStub(channel)

print("stub set ")
# Update this with desired payload
order = service_pb2.LocationMessage(
    id=3113,
    person_id=1,
    longitude='9.0',
    latitude='48.0',
    creation_time="2022-06-08T10:37:06"
)
print("creat lcoation message")
response = stub.Create(order)
print(response)

stub = service_pb2_grpc.PersonServiceStub(channel)
# Update this with desired payload
order = service_pb2.PersonMessage(
    id=4334,
    first_name="hainan",
    last_name='chen',
    company_name='mercedes ag'
)
print("creat person message")
response = stub.Create(order)
print(response)
