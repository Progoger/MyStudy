from generals.database import Database
from users.templates import GET_TEACHERS


def get_teachers(params):
    return Database(params['schema']).SqlQuery(GET_TEACHERS, params['lesson'])
