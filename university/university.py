from generals.database import Database
from university.templates import (GET_ALL_UNIVERSITIES, GET_ALL_DIRECTIONS)


def get_all_universities(params):
    return Database(params['schema']).SqlQuery(GET_ALL_UNIVERSITIES)


def get_all_directions(params):
    return Database(params['schema']).SqlQuery(GET_ALL_DIRECTIONS)

