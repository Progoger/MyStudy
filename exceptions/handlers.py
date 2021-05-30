from abc import ABC, abstractmethod
from generals.database import Database
from enum import Enum


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
    @abstractmethod
    def check_action(self, params):
        pass


class ExceptionsMessages(Enum):
    NAME_DUPLICATES = 'Невозможно вставить запись - обнаружены дупликаты'


class CheckGroupName(CheckErrorHandler):
    """
    Проверка на дублирование групп
    """
    def check(self, params, db_connect: Database):
        request = f"""select EXISTS(select null from "Group" where "Name" = %s or "ParentGroup" = %s)"""
        exists = db_connect.SqlQueryScalar(request, params['title'], params['title'])
        if exists:
            return ExceptionsMessages.NAME_DUPLICATES

