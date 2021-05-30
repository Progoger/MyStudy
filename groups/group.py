from generals.database import Database
from groups.templates import GET_ALL_GROUPS, GET_GROUPS_BY_DIRECTION, ADD_GROUP, CHECK_SUBGROUP_GROUP


def get_all_groups(params):
    return Database(params['schema']).SqlQuery(GET_ALL_GROUPS)


def get_groups_by_direction(params):
    res = Database(params['schema']).SqlQuery(GET_GROUPS_BY_DIRECTION, params['direction'])
    for elem in res:
        elem['id'] = elem['title']
    return res


def add_group(params):
    if params['type'] is None:
        groups = get_groups_by_direction(params)
        for group in groups:
            if group['title'] == params['title'] or group['parent'] == params['title']:
                break
        else:
            return Database(params['schema']).SqlQuery(ADD_GROUP, params['title'], None, params['direction'], None)
    else:
        return Database(params['schema']).SqlQuery(CHECK_SUBGROUP_GROUP, params['title'])
