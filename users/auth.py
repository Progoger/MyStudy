from generals.database import Database
from users.templates import (GET_DATA_BY_LOGIN, UPDATE_SESSION_BY_LOGIN, GET_USER_DATA_BY_SESSION,
                             CHECK_USER_TO_USE_CODE, UPDATE_STUDENT_GROUP_BY_CODE, CREATE_USER, CHECK_LOGIN)
from invites.invite import is_active_code
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import uuid


SYSTEM_ROLES = {
    'admin': '1c976561-577b-497e-9ce7-115275be3065',
    'student': '442f3a52-e9b1-4a27-b5f9-cb86438e1acf'
}
SYSTEM_ROLES_UUID = {
    '1c976561-577b-497e-9ce7-115275be3065': 'admin',
    '442f3a52-e9b1-4a27-b5f9-cb86438e1acf': 'student'
}


class User:
    """
    Класс для легкого взаимодействия с пользователями
    """
    def __init__(self, login=None, session=None, schema=None, old_session=None, university=None, color=None, role=None):
        self.login = login
        self.session = session
        self.schema = schema
        self.old_session = old_session
        self.university = university
        self.color = color
        self.error_code = None
        self.role = SYSTEM_ROLES_UUID.get(role)

    def get_info_for_web(self):
        """
        Этими данными мы будем дополнять запросы с бэка для
        :return:
        """
        return {
            'session': self.session,
            'university': self.university,
            'color': self.color,
            'role': self.role
        }.copy()

    def get_info_for_back(self):
        """
        Этими данными мы будем дополнять запросы с фронта для корректного выполнения
        :return:
        """
        return {
            'login': self.login,
            'session': self.session,
            'schema': self.schema,
            'role': self.role
        }.copy()

    def is_authorized(self):
        """
        Проверка на успешность авторизации
        :return:
        """
        return self.login and self.session and self.schema


def load_user_info(session):
    user_data = Database().SqlQueryRecord(GET_USER_DATA_BY_SESSION, session) if session else None
    if user_data:
        return User(
            user_data['Login'],
            str(user_data['Session']),
            user_data['Schema'],
            None,
            user_data['University'],
            user_data['Color'],
            user_data['Role']
        )
    else:
        return User(session=session)


def do_login(login, password):
    """
    Основной метод авторизации
    :param login: Логин с фронта
    :param password: Пароль с фронта
    :return: Класс User с основной информацией
    """
    db = Database()
    record = db.SqlQueryRecord(GET_DATA_BY_LOGIN, login)
    if record and check_password_hash(record['Password'], password):
        if record['Role'] != SYSTEM_ROLES['admin'] and Database(record['Schema']).SqlQueryScalar(CHECK_LOGIN, login):
            user = User(login)
            user.error_code = 101
            return user
        new_session = str(uuid.uuid4())
        db.SqlQuery(UPDATE_SESSION_BY_LOGIN, new_session, date.today(), login)
        user = User(login, new_session, record['Schema'], record['Session'], record['University'], record['Color'], record['Role'])
        return user
    else:
        user = User(login)
        user.error_code = 100
        return user


def get_root_session():
    return Database().SqlQueryScalar("""select "Session"::text from "Authorization" where "Login" = 'noordan'""")


def use_code(params):
    user_info = Database().SqlQueryRecord(GET_DATA_BY_LOGIN, params['login'])
    if user_info and check_password_hash(user_info['Password'], params['password']):
        db = Database(user_info['Schema'])
        record = db.SqlQueryRecord(CHECK_USER_TO_USE_CODE, params['login'])
        if record['can_activate'] and record['active_code']:
            db.SqlQuery(UPDATE_STUDENT_GROUP_BY_CODE, params['login'], params['login'], params['login'])
            return True

    return False


def register_person(params):
    """
    login, password, code, name, surname, patronymic, organization
    """
    params['schema'] = params['organization']
    db = Database(params['schema'])
    user_info = db.SqlQueryRecord(GET_DATA_BY_LOGIN, params['login'])
    if not user_info and is_active_code(params):
        db.SqlQuery(CREATE_USER, params['login'], generate_password_hash(params['password']),
                    params['organization'], uuid.uuid4(), params['login'], params['name'],
                    params['surname'], params['patronymic'], params['code'], params['code'],
                    params['code'])
        return True
    return False
