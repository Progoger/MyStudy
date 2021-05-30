import json
from flask import make_response
from abc import abstractmethod


class ActionExceptionHandler(Exception):
    """
    Базовый класс ошибки
    """
    @abstractmethod
    def get_response(self):
        """
        Возвращает ответ от сервера фронту в формате make_response
        """
        pass


class BeforeActionException(ActionExceptionHandler):
    """
    Ошибка предобработчика
    """
    def __init__(self, message):
        self._message = message
        self.error_code = 304

    def get_response(self):
        params = {
            'message': self._message
        }
        return make_response(json.dumps(params), self.error_code)
