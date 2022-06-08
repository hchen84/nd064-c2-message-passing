import grpc
import service_pb2
import service_pb2_grpc

"""
Sample implementation of a writer that can be used to write messages to gRPC.
"""

print("Sending sample payload...")

channel = grpc.insecure_channel("localhost:30002")
stub = service_pb2_grpc.LocationServiceStub(channel)

response = stub.Get(service_pb2.Empty())
print(response)
