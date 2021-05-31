from generals.database import Database
from lessons.templates import GET_LESSONS, ADD_LESSON, DELETE_LESSON, EDIT_LESSON
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
