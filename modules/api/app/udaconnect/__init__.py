from app.udaconnect.models import Connection, Location, Person  # noqa
from app.udaconnect.schemas import ConnectionSchema, LocationSchema, PersonSchema  # noqa
import os

import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("udaconnect-api")


def register_routes(api, app, root="api"):
    if "APP" in os.environ and os.environ["APP"] == "location":
        from modules.api.app.udaconnect.controllers_location import api as udaconnect_location_api
        api.add_namespace(udaconnect_location_api, path=f"/{root}")
        logging.INFO("App Location started")
    else:
        from modules.api.app.udaconnect.controllers_person import api as udaconnect_person_api
        api.add_namespace(udaconnect_person_api, path=f"/{root}")
        logging.INFO("App person started")
