from generals.database import Database
from groups.templates import *


def get_all_groups(params):
    return Database(params['schema']).SqlQuery(GET_ALL_GROUPS)


def get_groups_by_direction(params):
    res = Database(params['schema']).SqlQuery(GET_GROUPS_BY_DIRECTION, params['direction'])
    for elem in res:
        elem['id'] = elem['title']
    return res


def get_subgroups_by_group(params):
    return Database(params['schema']).SqlQuery(GET_GROUPS_BY_PARENTGROUP, params['id'])


def add_group(params):
    if params['type'] is None:
        check = Database(params['schema']).SqlQuery(CHECK_GROUP_EXIST, params['title'], params['title'])
        if len(check) > 0:
            return Database(params['schema']).SqlQuery(ADD_GROUP, params['title'], None, params['direction'], None)
    else:
        check = Database(params['schema']).SqlQuery(CHECK_SUBGROUP_GROUP, params['title'])
        if len(check) > 0:
            return Database(params['schema']).SqlQuery(UPDATE_GROUP_TO_SUBGROUP, params['title'], params['type'])
        else:
            return Database(params['schema']).SqlQuery(
                ADD_GROUP,
                params['title']+params['type'],
                params['title'],
                params['direction'],
                params['type'])
