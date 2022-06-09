import grpc
import service_pb2
import service_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("0.0.0.0:gprc")
stub = service_pb2_grpc.LocationServiceStub(channel)

# Update this with desired payload
order = service_pb2.LocationMessage(
    id=3222,
    person_id=1,
    longitude='9',
    latitude='48',
    creation_time='2020-08-18T10:37:06'
)
response = stub.Create(order)

stub = service_pb2_grpc.PersonServiceStub(channel)
# Update this with desired payload
order = service_pb2.PersonMessage(
    id=3222,
    first_name="hainan",
    last_name='chen',
    company_name='mercedes'
)
response = stub.Create(order)
