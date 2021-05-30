from generals.database import Database
from exceptions.handlers import ActionErrorCheckHandler, CheckGroupName
from exceptions.exception import BeforeActionException


class CheckMethodAddGroup(ActionErrorCheckHandler):
    """
    Проверка метода добавления групп
    """
    def __init__(self):
        self._methods_to_check = [CheckGroupName]

    def check_action(self, params):
        db_connect = Database(params['schema'])
        for handler in self._methods_to_check:
            error_message = handler().check(params, db_connect)
            if error_message:
                raise BeforeActionException(error_message)
