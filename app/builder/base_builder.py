import tarfile
import os
import json
from distutils.dir_util import copy_tree

from app.base import Base


class BaseBuilder(Base):

    def __init__(self, bot_id):
        super(BaseBuilder, self).__init__()
        self._bot_id = bot_id

    def build(self, *args, **kwargs):
        raise NotImplementedError

    def _get_bot(self):
        bot = self._translate_db.select('bots',
                                        where_statements={'id': self._bot_id},
                                        return_dict=True)
        if len(bot) == 0:
            raise Exception(f'No such bot: {self._bot_id}')
        bot = bot[0]
        return {
            'phrases': self._get_bot_phrases(bot),
            'file_name': bot.get('file_name'),
            'lang': bot.get('lang')
        }

    def _get_bot_phrases(self, bot):
        phrases_ids = self._get_bot_phrases_ids()
        phrases_ids_join = f'({", ".join(str(phrase_id) for phrase_id in phrases_ids)})'
        bot_phrases = self._translate_db.select('phrases',
                                                where_statements={'id': ['in', phrases_ids_join]},
                                                return_all=True,
                                                return_dict=True)
        return bot_phrases

    def _get_bot_phrases_ids(self):
        bot_phrases_ids = []
        for build_table in self._tables:
            phrases_ids = self.__get_table_phrases_ids(build_table) or []
            bot_phrases_ids += phrases_ids
        return bot_phrases_ids

    def __get_table_phrases_ids(self, build_table):
        table_phrases_ids = []
        table_name = build_table.get('name')
        table_rows = self._translate_db.select(table_name,
                                               where_statements={'bot_id': self._bot_id},
                                               return_dict=True,
                                               return_all=True)
        if len(table_rows) != 0:
            table_phrases_ids += self.process_tables(table_rows, build_table.get('children'))
            return table_phrases_ids
        return

    def process_tables(self, table_rows, children):
        ids = []
        for table_row in table_rows:
            ids.append(table_row.get('phrase_id'))
            ids += self.__process_children(children, table_row.get('id'))
        return ids

    def __process_children(self, children, parent_id):
        ids = []
        for child in children:
            ids += self.__get_child_phrases_ids(child, parent_id)
        return ids

    def __get_child_phrases_ids(self, child, parent_id):
        parent_column = child.get('parent_column')
        child_rows = self._translate_db.select(child['name'],
                                               where_statements={parent_column: parent_id},
                                               return_all=True,
                                               return_dict=True)
        return [child.get('phrase_id') for child in child_rows]

    @staticmethod
    def _copy_bot(bot_id):
        copy_tree(f'app/work_data/bots/{bot_id}', 'app/work_data/tmp')

    @staticmethod
    def _rewrite_json_file(path, content):
        if os.path.exists(path):
            with open(path, 'w') as f:
                json.dump(content, f)

    @staticmethod
    def _zip(file_name):
        path = f'app/work_data/out/bots/{file_name}'
        with tarfile.open(path, "w:gz") as tar:
            tar.add('app/work_data/tmp', arcname=os.path.basename('app/work_data/tmp'))
