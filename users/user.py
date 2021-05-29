from generals.database import Database
from users.templates import GET_TEACHERS, GET_TEACHERS_BY_INSTITUTE, INSERT_TEACHER
from uuid import uuid4


def get_teachers(params):
    return Database(params['schema']).SqlQuery(GET_TEACHERS, params['lesson'])


def get_teachers_by_institute(params):
    return Database(params['schema']).SqlQuery(GET_TEACHERS_BY_INSTITUTE, params['institute'])


def add_teacher(params):
    return Database(params['schema']).SqlQueryRecord(
        INSERT_TEACHER,
        uuid4(),
        params['name'],
        params['surname'],
        params['patronymic'],
        params['direction']
    )