from generals.database import Database
from university.templates import *
from uuid import uuid4


def get_all_institutes(params):
    return Database(params['schema']).SqlQuery(GET_ALL_INSTITUTES, params['organisation'])


def get_directions(params):
    return Database(params['schema']).SqlQuery(GET_DIRECTIONS, params['institute'])


def add_direction(params):
    return Database(params['schema']).SqlQueryRecord(ADD_DIRECTION, uuid4(), params['title'], params['institute'])


def add_institute(params):
    return Database(params['schema']).SqlQueryRecord(ADD_INSTITUTE, uuid4(), params['title'])


def del_institute(params):
    return Database(params['schema']).SqlQueryRecord(DEL_INSTITUTE, params['id'])


def del_direction(params):
    return Database(params['schema']).SqlQueryRecord(DEL_DIRECTION, params['id'])


def edit_direction(params):
    return Database(params['schema']).SqlQueryRecord(EDIT_DIRECTION, params['title'], params['id'])


def edit_institute(params):
    return Database(params['schema']).SqlQueryRecord(EDIT_INSTITUTE, params['title'], params['id'])
