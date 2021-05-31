from abc import ABC, abstractmethod
from generals.database import Database
from exceptions.exception import ExceptionsMessages


class CheckErrorHandler(ABC):
    """
    Интерфейс обработчика поиска ошибок
    """
    @abstractmethod
    def check(self, params, db_connect):
        pass


class ActionErrorCheckHandler(ABC):
    """
    Интерфейс поиска ошибок в методах. Содержит перечисление проверок CheckErrorHandler
    """
    def __init__(self):
        self._methods_to_check = []

    def del_check(self, name):
        """
        Удалить нужную проверку из списка
        """
        if name in self._methods_to_check:
            self._methods_to_check.remove(name)

    @abstractmethod
    def check_action(self, params):
        pass


class CheckGroupName(CheckErrorHandler):
    """
    Проверка на дублирование групп
    """
    def check(self, params, db_connect: Database):
        if params['type']:
            request = f"""select EXISTS(select null from "Group" where "Name" = %s or ("ParentGroup" = %s and "Type" = %s))"""
            exists = db_connect.SqlQueryScalar(request, params['title']+params['type'], params['title'], params['type'])
        else:
            request = f"""select EXISTS(select null from "Group" where "Name" = %s or "ParentGroup" = %s)"""
            exists = db_connect.SqlQueryScalar(request, params['title'], params['title'])
        if exists:
            return ExceptionsMessages.NAME_DUPLICATES
