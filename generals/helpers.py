from generals.templates import GET_SCHEMA_BY_SESSION
from generals.database import Database


def get_schema_by_session(session):
    return Database().SqlQueryScalar(GET_SCHEMA_BY_SESSION, session)

