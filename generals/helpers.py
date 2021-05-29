from generals.templates import GET_SCHEMA_BY_SESSION
from generals.database import Database
import json
from uuid import UUID


def get_schema_by_session(session):
    return Database().SqlQueryScalar(GET_SCHEMA_BY_SESSION, session)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            # if the obj is uuid, we simply return the value of uuid
            return obj.hex
        return json.JSONEncoder.default(self, obj)
