from generals.database import Database
from users.templates import GET_TEACHERS, GET_TEACHERS_BY_INSTITUTE, ADD_TEACHER, ADD_TEACHER_TO_LESSON, DELETE_TEACHERS_FROM_LESSON
from uuid import uuid4


def get_teachers(params):
    return Database(params['schema']).SqlQuery(GET_TEACHERS, params['id'])


def get_teachers_by_institute(params):
    return Database(params['schema']).SqlQuery(GET_TEACHERS_BY_INSTITUTE, params['institute'])


def add_teacher(params):
    return Database(params['schema']).SqlQueryRecord(
        ADD_TEACHER,
        uuid4(),
        params['name'],
        params['surname'],
        params['patronymic'],
        params['direction']
    )


def update_teachers_lesson(params):
    Database(params['schema']).SqlQuery(DELETE_TEACHERS_FROM_LESSON, params['lesson'])
    teachers = params['tutors']
    for teacher in teachers:
        Database(params['schema']).SqlQueryRecord(ADD_TEACHER_TO_LESSON, params['lesson'], teacher['id'])
    return params