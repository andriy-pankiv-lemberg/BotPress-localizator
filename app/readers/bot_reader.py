from os import listdir
from os.path import isfile, join

from app.readers.base_reader import BaseReader
from app.readers.card_reader import CardReader
from app.readers.text_reader import TextReader
from app.readers.single_choice_reader import SingleChoiceReader


class BotReader(BaseReader):

    def __init__(self, file_name):
        super(BotReader, self).__init__()
        self._file_name = file_name

    def read(self):
        existed_bot = self._translate_db.select('bots',
                                                where_statements={'file_name': self._file_name},
                                                return_dict=True)
        if len(existed_bot) == 0:
            bot_id = self._create_bot()
            self._unzip(bot_id)
            self._fill_content(bot_id)
        else:
            existed_bot = existed_bot[0]
            self._edit_bot(existed_bot.get('id'))

    def _edit_bot(self, bot_id):
        self._clear_bot(bot_id)
        self._fill_content(bot_id)

    def _fill_content(self, bot_id):
        content_elements = self._read_content(bot_id)
        for element in content_elements:
            if element in self._readers:
                eval(self._readers[element].get('class'))(bot_id).read()

    def _clear_bot(self, bot_id):
        for reader_table in [self._readers[name].get('table_name') for name in list(self._readers.keys())]:
            self._translate_db.delete(reader_table,
                                      where_statements={'bot_id': bot_id})

    def _read_content(self, bot_id):
        only_files = [
            f for f in listdir(f'app/work_data/bots/{bot_id}/content-elements/')
            if isfile(join(f'app/work_data/bots/{bot_id}/content-elements/', f))
        ]
        return [self.__clear_content_name(content_name) for content_name in only_files]

    @staticmethod
    def __clear_content_name(content_name):
        return content_name.replace('builtin_', '').replace('.json', '')
