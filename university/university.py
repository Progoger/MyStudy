from generals.database import Database
from university.templates import (GET_ALL_INSTITUTES, GET_DIRECTIONS, ADD_DIRECTION, ADD_INSTITUTE)
from uuid import uuid4


def get_all_institutes(params):
    return Database(params['schema']).SqlQuery(GET_ALL_INSTITUTES)


def get_directions(params):
    return Database(params['schema']).SqlQuery(GET_DIRECTIONS, params['institute'])


def add_direction(params):
    return Database(params['schema']).SqlQuery(ADD_DIRECTION, uuid4(), params['title'], params['institute'])


def add_institute(params):
    return Database(params['schema']).SqlQuery(ADD_INSTITUTE, uuid4(), params['title'])
