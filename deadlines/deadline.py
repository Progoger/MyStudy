from generals.database import Database
from deadlines.templates import *
from uuid import uuid4
import datetime


def create_deadline(params):
    db = Database(params['schema'])
    res = db.SqlQueryRecord(CREATE_DEADLINE, uuid4(), params['id'], params['text'], datetime.datetime.now(), 'обсудить с Ромой, как он отдаёт дату')
    db.SqlQuery(ADD_USER_TO_DEADLINE, res['id'], params['id'])


def get_deadline(params):
    db = Database(params['schema'])
    res = db.SqlQuery(GET_DEADLINES, params['id'])
