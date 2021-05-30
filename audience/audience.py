from generals.database import Database
from audience.templates import GET_AUDIENCES, ADD_AUDIENCES


def get_audiences(params):
    return Database(params['schema']).SqlQuery(GET_AUDIENCES, params['id'])


def add_audiences(params):
    return Database(params['schema']).SqlQuery(ADD_AUDIENCES, params['id'], params['housing_id'])
