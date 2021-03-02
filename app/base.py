import json
import os

from app.configs import TranslateDB
from db.connector import DBConnector


class Base:

    def __init__(self):
        self._translate_db = None
        self._connect_to_db()
        self._tables = [
            {
                'name': 'cards',
                'file_match': 'card',
                'children': [
                    {
                        'name': 'actions',
                        'parent_column': 'card_id'
                    }
                ]
            },
            {
                'name': 'single_choices',
                'file_match': 'single-choice',
                'children': [
                    {
                        'name': 'choices',
                        'parent_column': 'single_choice_id'
                    }
                ]
            },
            {
                'name': 'texts',
                'file_match': 'text',
                'children': [
                    {
                        'name': 'variations',
                        'parent_column': 'text_id'
                    }
                ]
            }
        ]

    def _load_rows(self, rows):
        self._rows = rows
        return self._generate_bot_structure()

    def _generate_bot_structure(self):
        bot_structure = []
        for i, row in enumerate(self._rows):
            for table in self._tables:
                tmp = {
                    'name': table.get('name')
                }
                element_row = self._translate_db.select(table.get('name'),
                                                        where_statements={'phrase_id': row.get('id')},
                                                        return_dict=True)
                if len(element_row) != 0:
                    element_row = element_row[0]
                    tmp['row'] = element_row
                    tmp['children'] = []
                    for child_table in table.get('children'):
                        tmp_child = {
                            'name': child_table.get('name')
                        }
                        children_rows = self._translate_db.select(child_table.get('name'),
                                                                  where_statements={
                                                                      child_table.get('parent_column'): element_row.get(
                                                                          'id')},
                                                                  return_dict=True,
                                                                  return_all=True)
                        tmp_child['rows'] = children_rows
                        tmp['children'].append(tmp_child)
                    bot_structure.append(tmp)
        return bot_structure

    @staticmethod
    def _rename_schema(schema, lang, new_lang):
        return json.dumps(schema).replace(f'${lang}', f'${new_lang}')

    @staticmethod
    def _remove_extension(file_name):
        return file_name.split('.')[0]

    @staticmethod
    def _empty_folder(path):
        if os.path.exists(path):
            for filename in os.listdir(path):
                os.remove(filename)

    @staticmethod
    def _read_file(path):
        with open(path) as f:
            file = f.read()
        return file

    def _find_table_match(self, table_name):
        return next((table for table in self._tables if table['name'] == table_name), None)

    def _get_parent_bot_id(self, file_name):
        clean_name = self._remove_extension(file_name)
        return int(clean_name.split('-')[-1])

    def _connect_to_db(self):
        self._translate_db = DBConnector(TranslateDB)

