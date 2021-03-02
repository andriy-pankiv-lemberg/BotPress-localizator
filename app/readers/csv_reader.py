import json
import csv

from app.readers.base_reader import BaseReader


class CsvReader(BaseReader):

    def __init__(self, file_name, new_bot_languages=None):
        super(CsvReader, self).__init__()
        self._file_name = file_name
        self._rows = None
        self._new_bot_languages = new_bot_languages
        self._copy_methods = {
            'cards': '_copy_card',
            'single_choices': '_copy_single_choice',
            'texts': '_copy_text',
        }

    def read(self):
        rows = self._read_csv()
        bot_structure = self._load_rows(rows)
        return self._create_bots(bot_structure)

    def _create_bots(self, bot_structure):
        new_bots = []
        for new_bot_lang in self._new_bot_languages:
            tmp = {
                'lang': new_bot_lang
            }
            bot_id = self._create_bot(new_bot_lang)
            tmp['id'] = bot_id
            self._copy_bot(bot_structure, bot_id, new_bot_lang)
            new_bots.append(tmp)
        return new_bots

    def _copy_bot(self, bot_structure, bot_id, new_bot_lang):
        self._generate_bot(bot_structure, bot_id, new_bot_lang)

    def _generate_bot(self, bot_structure, bot_id, new_bot_lang):
        for bot_element in bot_structure:
            translation_row = self._find_row_by_phase_id(bot_element['row']['phrase_id'])
            getattr(self, self._copy_methods[bot_element.get('name')])(bot_element, translation_row, bot_id, new_bot_lang)

    def _copy_card(self, bot_element, card, bot_id, new_bot_lang):
        original_card = bot_element.get('row')
        card_copy = {
            'id': original_card.get('element_id'),
            'title': card.get(new_bot_lang),
            'schema': self._rename_schema(original_card.get('schema'), original_card.get('lang'), new_bot_lang)
        }
        card_id = self._create_card(card_copy, bot_id, new_bot_lang)
        for child in bot_element.get('children'):
            for row in child.get('rows'):
                translation_row = self._find_row_by_phase_id(row.get('phrase_id'))
                action_copy = {
                    'title': translation_row.get(new_bot_lang),
                }
                self._create_action(action_copy, card_id, new_bot_lang)

    def _copy_single_choice(self, bot_element, single_choice, bot_id, new_bot_lang):
        pass

    def _copy_text(self, bot_element, text, bot_id, new_bot_lang):
        original_text = bot_element.get('row')
        text_copy = {
            'id': original_text.get('element_id'),
            'text': text.get(new_bot_lang),
            'schema': self._rename_schema(original_text.get('schema'), original_text.get('lang'), new_bot_lang)
        }
        text_id = self._create_text(text_copy, bot_id, new_bot_lang)
        for child in bot_element.get('children'):
            for row in child.get('rows'):
                translation_row = self._find_row_by_phase_id(row.get('phrase_id'))
                variation_copy = {
                    'text': translation_row.get(new_bot_lang),
                }
                self._create_variation(variation_copy, text_id, new_bot_lang)

    def _read_csv(self):
        with open(f'app/work_data/in/csv/{self._file_name}') as f:
            csv_reader = csv.reader(f, delimiter=',')
            columns = next(csv_reader)
            if self._new_bot_languages is None:
                self._new_bot_languages = self._get_new_bot_languages(columns)
            rows = [{columns[i]: row[i] for i in range(len(columns))} for row in csv_reader]
        return rows

    @staticmethod
    def _get_new_bot_languages(columns):
        return columns[2:]

    def _find_row_by_phase_id(self, phrase_id):
        return next((row for row in self._rows if row["id"] == str(phrase_id)), None)
