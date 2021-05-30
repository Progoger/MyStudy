from generals.database import Database
from housing.templates import GET_ALL_HOUSING, ADD_HOUSING, EDIT_ADDRESS


def get_all_housing(params):
    return Database(params['schema']).SqlQuery(GET_ALL_HOUSING)


def add_housing(params):
    return Database(params['schema']).SqlQueryRecord(ADD_HOUSING, params['id'], params['address'])


def edit_housing_address(params):
    Database(params['schema']).SqlQuery(EDIT_ADDRESS, params['address'], params['id'])
