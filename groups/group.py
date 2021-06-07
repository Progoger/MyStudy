from generals.database import Database
from groups.templates import *


def get_all_groups(params):
    return Database(params['schema']).SqlQuery(GET_ALL_GROUPS)


def get_groups_by_direction(params):
    res = Database(params['schema']).SqlQuery(GET_GROUPS_BY_DIRECTION, params['direction'])
    for elem in res:
        elem['id'] = elem['title']
    return res


def get_groups_by_institute_year(params):
    res = Database(params['schema']).SqlQuery(GET_GROUPS_BY_INSTITUTE_YEAR, params['institute'], params['year'][0:2]+'%')
    for elem in res:
        elem['id'] = elem['title']
    return res


def get_subgroups_by_group(params):
    res = Database(params['schema']).SqlQuery(GET_GROUPS_BY_PARENTGROUP, params['id'])
    for elem in res:
        elem['title'] = elem['id']
    return res


def add_group(params):
    check = Database(params['schema']).SqlQuery(CHECK_GROUP_EXIST, params['title'], params['title'])
    if len(check) == 0:
        res = Database(params['schema']).SqlQueryRecord(ADD_GROUP, params['title'], None, params['direction'], None)
        res['title'] = res['id']
        return res


def add_subgroup(params):
    db = Database(params['schema'])
    check = db.SqlQuery(CHECK_SUBGROUP_GROUP, params['masterItem']['title'])
    if len(check) > 0:
        res = db.SqlQueryRecord(
            UPDATE_GROUP_TO_SUBGROUP,
            params['masterItem']['title']+params['body']['title'],
            params['body']['title'],
            params['masterItem']['title']
        )
        res['title'] = res['id']
        return res
    else:
        res = db.SqlQueryRecord(
            ADD_GROUP,
            params['masterItem']['title']+params['body']['title'],
            params['masterItem']['title'],
            params['body']['direction'],
            params['body']['title'])

        res['title'] = res['id']
        return res


def delete_group(params):
    db = Database(params['schema'])
    db.SqlQuery(DELETE_GROUP, params['id'])


def delete_subgroup(params):
    db = Database(params['schema'])
    db.SqlQuery(DELETE_SUBGROUP, params['id'])
