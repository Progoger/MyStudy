from generals.database import Database
from users.templates import GET_PASSWORD_BY_LOGIN, UPDATE_SESSION_BY_LOGIN
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import date
import uuid


class User:
    """
    Класс для легкого взаимодействия с пользователями
    """
    def __init__(self, login, session, schema, old_session):
        self.login = login
        self.session = session
        self.schema = schema
        self.old_session = old_session

    def get_info(self):
        """
        Этими данными мы будем дополнять запросы с фронта для корректного выполнения
        :return:
        """
        return {
            'login': self.login,
            'session': self.session,
            'schema': self.schema,
            'old_session': self.old_session
        }

    def is_authorized(self):
        """
        Проверка на успешность авторизации
        :return:
        """
        if self.login and self.session and self.schema:
            return True
        else:
            return False


def do_login(login, password):
    """
    Основной метод авторизации
    :param login: Логин с фронта
    :param password: Пароль с фронта
    :return: Класс User с основной информацией
    """
    record = Database().SqlQueryRecord(GET_PASSWORD_BY_LOGIN, login)
    if record and check_password_hash(record['Password'], password):
        new_session = str(uuid.uuid4())
        Database().SqlQuery(UPDATE_SESSION_BY_LOGIN, new_session, date.today(), login)
        return User(login, new_session, record['Schema'], record['Session'])
    else:
        return User(login, None, None, None)
