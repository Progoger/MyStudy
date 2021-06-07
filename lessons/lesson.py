from generals.database import Database
from lessons.templates import GET_LESSONS, ADD_LESSON, DELETE_LESSON, EDIT_LESSON, ADD_LESSON_TYPE, GET_LESSON_TYPES, EDIT_LESSON_TYPE, DELETE_LESSON_TYPE
from users.templates import GET_TEACHERS
from uuid import uuid4


def get_lessons(params):
    db = Database(params['schema'])
    main = db.SqlQuery(GET_LESSONS, params['direction'])
    for lesson in main:
        lesson['tutors'] = db.SqlQuery(GET_TEACHERS, lesson['id'])
    return main


def add_lesson(params):
    res = Database(params['schema']).SqlQueryRecord(ADD_LESSON, uuid4(), params['title'], params['direction'])
    res['tutors'] = []
    return res


def delete_lesson(params):
    Database(params['schema']).SqlQuery(DELETE_LESSON, params['id'])
    return params['id']


def edit_lesson(params):
    return Database(params['schema']).SqlQueryRecord(EDIT_LESSON, params['title'], params['id'])


def add_lesson_type(params):
    res = Database(params['schema']).SqlQueryRecord(ADD_LESSON_TYPE, uuid4(), params['name'], params['logoType'])
    return res


def get_lesson_types(params):
    return Database(params['schema']).SqlQuery(GET_LESSON_TYPES)


def edit_lesson_type(params):
    return Database(params['schema']).SqlQuery(EDIT_LESSON_TYPE, params['name'], params['logoType'], params['type'])


def delete_lesson_type(params):
    return Database(params['schema']).SqlQuery(DELETE_LESSON_TYPE, params['type'])
