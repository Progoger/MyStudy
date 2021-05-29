from generals.database import Database
from groups.templates import GET_ALL_GROUPS


def get_all_groups(params):
    return Database(params['schema']).SqlQuery(GET_ALL_GROUPS)