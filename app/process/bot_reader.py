from db.connector import DBConnector
from app.decorators import decorate_all_methods, ErrorDefender
from app.configs import TranslateDB


@decorate_all_methods(ErrorDefender)
class BotReader:

    def __init__(self, config):
        self._config = config
        self.translate_db = None
        self.__connect_to_db()

    def read(self):
        pass

    def __connect_to_db(self):
        self.translate_db = DBConnector(TranslateDB)
