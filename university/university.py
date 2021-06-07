from generals.database import Database
from university.templates import *
from uuid import uuid4


def get_all_institutes(params):
    return Database(params['schema']).SqlQuery(GET_ALL_INSTITUTES, params['organisation'])


def get_directions(params):
    return Database(params['schema']).SqlQuery(GET_DIRECTIONS, params['institute'])


def get_directions_with_groups(params):
    res = Database(params['schema']).SqlQuery(GET_DIRECTIONS_WITH_GROUPS, params['institute'])
    directions = []
    groups = []
    types = []
    if len(res) > 0:
        last_direction_id = res[0]['directionId']
        last_direction = res[0]['direction']
        if res[0]['group']:
            last_group = res[0]['group']
        else:
            last_group = res[0]['subgroup']
        direction = {}
        group = {}
        for elem in res:
            if last_direction_id != elem['directionId']:
                group['types'] = types
                group['name'] = last_group
                if group != {}:
                    groups.append(group)
                direction['id'] = last_direction_id
                direction['title'] = last_direction
                direction['groups'] = groups
                directions.append(direction)
                types = []
                direction = {}
                groups = []
                group = {}
                last_group = elem['group']
                last_direction_id = elem['directionId']
                last_direction = elem['direction']
            if elem['group'] and last_group != elem['group'] or not elem['group'] and last_group != elem['subgroup']:
                group['types'] = types
                group['name'] = last_group
                groups.append(group)
                group = {}
                types = []
                if elem['group']:
                    last_group = elem['group']
                else:
                    last_group = elem['subgroup']
            if elem['group']:
                types.append(elem['subgroup'][-1])
            else:
                elem['group'] = elem['subgroup']
        group['types'] = types
        group['name'] = last_group
        groups.append(group)
        direction['id'] = last_direction_id
        direction['title'] = last_direction
        direction['groups'] = groups
        directions.append(direction)
    return directions


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
