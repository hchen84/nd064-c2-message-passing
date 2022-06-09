from asyncio.log import logger
from datetime import datetime

from app.udaconnect.models import Connection, Location, Person
from app.udaconnect.schemas import (
    ConnectionSchema,
    LocationSchema,
    PersonSchema,
)
from app.udaconnect.services import ConnectionService, LocationService, PersonService
from flask import request, g
from flask_accepts import accepts, responds
from flask_restx import Namespace, Resource
from typing import Optional, List

import grpc
from app.service_pb2 import LocationMessage, PersonMessage
import app.service_pb2_grpc
from app.service_pb2_grpc import PersonServiceStub, LocationServiceStub

import json

DATE_FORMAT = "%Y-%m-%d"

api = Namespace("UdaConnect", description="Connections via geolocation.")  # noqa

channel = grpc.insecure_channel("localhost:30002")
# location_stub = LocationServiceStub(channel)
person_stub = PersonServiceStub(channel)
# # TODO: This needs better exception handling


# @api.route("/locations")
# class LocationResource(Resource):
#     @accepts(schema=LocationSchema)
#     # @responds(schema=LocationSchema)
#     def post(self) -> Location:
#         payload = request.get_json()
#         # location: Location = LocationService.create(payload)

#         print("start to send a location to grpc")
#         global location_stub
#         msg = LocationMessage(
#             id=0,  # payload["id"],
#             person_id=payload["person_id"],
#             longitude=payload["longitude"],
#             latitude=payload["latitude"],
#             creation_time=payload["creation_time"]
#         )
#         response = location_stub.Create(msg)
#         print("sent a location grpc")
#         return response

#     @responds(schema=LocationSchema, many=True)
#     def get(self) -> List[Location]:
#         locations: Location = LocationService.retrieve_all()
#         return locations


# @api.route("/locations/<location_id>")
# @api.param("location_id", "Unique ID for a given Location", _in="query")
# class LocationResource(Resource):
#     @responds(schema=LocationSchema)
#     def get(self, location_id) -> Location:
#         location: Location = LocationService.retrieve(location_id)
#         return location


@api.route("/persons")
class PersonsResource(Resource):
    @accepts(schema=PersonSchema)
    # @responds(schema=PersonSchema)
    def post(self) -> Person:
        payload = request.get_json()
        # new_person: Person = PersonService.create(payload)

        print("start to send a person to grpc")
        global person_stub
        msg = PersonMessage(
            id=0,  # payload["id"],
            first_name=payload["first_name"],
            last_name=payload["last_name"],
            company_name=payload["company_name"]
        )
        response = person_stub.Create(msg)
        print("sent a person grpc")
        return response

    @responds(schema=PersonSchema, many=True)
    def get(self) -> List[Person]:
        persons: List[Person] = PersonService.retrieve_all()
        return persons


@api.route("/persons/<person_id>")
@api.param("person_id", "Unique ID for a given Person", _in="query")
class PersonResource(Resource):
    @responds(schema=PersonSchema)
    def get(self, person_id) -> Person:
        person: Person = PersonService.retrieve(person_id)
        return person


@api.route("/persons/<person_id>/connection")
@api.param("start_date", "Lower bound of date range", _in="query")
@api.param("end_date", "Upper bound of date range", _in="query")
@api.param("distance", "Proximity to a given user in meters", _in="query")
class ConnectionDataResource(Resource):
    @responds(schema=ConnectionSchema, many=True)
    def get(self, person_id) -> ConnectionSchema:
        start_date: datetime = datetime.strptime(
            request.args["start_date"], DATE_FORMAT
        )
        end_date: datetime = datetime.strptime(
            request.args["end_date"], DATE_FORMAT)
        distance: Optional[int] = request.args.get("distance", 5)

        results = ConnectionService.find_contacts(
            person_id=person_id,
            start_date=start_date,
            end_date=end_date,
            meters=distance,
        )
        return results
