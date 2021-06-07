from generals.database import Database
from invites.templates import GENERATE_CODES, IS_ACTIVE_CODE, DEL_CODE
from secrets import token_hex


def generate_codes(params):
    codes = [str(token_hex(5)) for i in range(int(params['count']))]
    return Database(params['schema']).SqlQuery(GENERATE_CODES, params['title'], codes)


def is_active_code(params):
    return Database(params['schema']).SqlQueryScalar(IS_ACTIVE_CODE, params['code'])


def del_code(params):
    return Database(params['schema']).SqlQuery(DEL_CODE, params['code'])
