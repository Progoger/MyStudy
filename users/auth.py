from generals.database import Database
from users.templates import GET_DATA_BY_LOGIN, UPDATE_SESSION_BY_LOGIN, GET_USER_DATA_BY_SESSION
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import uuid


class User:
    """
    Класс для легкого взаимодействия с пользователями
    """
    def __init__(self, login=None, session=None, schema=None, old_session=None, university=None, color=None):
        self.login = login
        self.session = session
        self.schema = schema
        self.old_session = old_session
        self.university = university
        self.color = color

    def get_info_for_web(self):
        """
        Этими данными мы будем дополнять запросы с бэка для
        :return:
        """
        return {
            'session': self.session,
            'university': self.university,
            'color': self.color
        }.copy()

    def get_info_for_back(self):
        """
        Этими данными мы будем дополнять запросы с фронта для корректного выполнения
        :return:
        """
        return {
            'login': self.login,
            'session': self.session,
            'schema': self.schema
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
            user_data['Color']
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
    record = Database().SqlQueryRecord(GET_DATA_BY_LOGIN, login)
    if record and check_password_hash(record['Password'], password):
        new_session = str(uuid.uuid4())
        Database().SqlQuery(UPDATE_SESSION_BY_LOGIN, new_session, date.today(), login)
        return User(login, new_session, record['Schema'], record['Session'], record['University'], record['Color'])
    else:
        return User(login)
