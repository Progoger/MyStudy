from generals.database import Database
from audience.templates import GET_AUDIENCES, ADD_AUDIENCES


def get_audiences(params):
    return Database(params['schema']).SqlQuery(GET_AUDIENCES, params['id'])


def add_audience(params):
    return Database(params['schema']).SqlQueryRecord(ADD_AUDIENCES, params['masterItem']['id'], params['body']['id'])
