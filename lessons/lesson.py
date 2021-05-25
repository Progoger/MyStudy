from generals.database import Database
from lessons.templates import GET_LESSONS, ADD_LESSON
from uuid import uuid4


def get_lessons(params):
    return Database(params['schema']).SqlQuery(GET_LESSONS, params['direction'])


def add_lesson(params):
    Database(params['schema']).SqlQuery(ADD_LESSON, uuid4(), params['title'], params['direction'])

