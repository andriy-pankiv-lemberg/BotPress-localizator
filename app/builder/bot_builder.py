import json
from copy import deepcopy

from app.builder.base_builder import BaseBuilder


class BotBuilder(BaseBuilder):

    def __init__(self, bot_id):
        super(BotBuilder, self).__init__(bot_id)
        self._build_functions = {
            'cards': '_build_card',
            'texts': '_build_text'
        }

    def build(self, new_bot_name):
        bot = self._get_bot()
        self._generate_bot(bot)
        self._zip(new_bot_name)

    def _generate_bot(self, bot_info):
        bot_structure = self._load_rows(bot_info.get('phrases'))
        bot = self._build_bot(bot_structure)
        self._copy_bot(self._get_parent_bot_id(bot_info.get('file_name')))
        self._set_bot_lang(bot_info.get('lang'))
        for bot_element in bot:
            table_match = self._find_table_match(bot_element)
            self._rewrite_json_file(f'app/work_data/tmp/content-elements/builtin_{table_match.get("file_match")}.json',
                                    bot.get(bot_element))

    def _build_bot(self, bot_structure):
        bot = {}
        for bot_element in bot_structure:
            element_name = bot_element.get('name')
            if element_name in bot:
                bot[element_name].append(getattr(self, self._build_functions.get(bot_element.get('name')))(bot_element))
            else:
                bot[element_name] = [getattr(self, self._build_functions.get(bot_element.get('name')))(bot_element)]
        return bot

    @staticmethod
    def _build_card(card):
        card_row = card["row"]
        json_structure = deepcopy(card_row['schema'])
        json_structure['formData'][f'title${card_row["lang"]}'] = card_row["title"]
        for child in card.get('children'):
            child_copy = deepcopy(json_structure['formData'][f'{child.get("name")}${card_row["lang"]}'])
            child_list = []
            for row, element in zip(child['rows'], child_copy):
                element['title'] = row['title']
                child_list.append(element)
            json_structure['formData'][f'{child.get("name")}${card_row["lang"]}'] = child_list
        return json_structure

    @staticmethod
    def _build_text(text):
        text_row = text["row"]
        json_structure = deepcopy(text_row['schema'])

        json_text = json.loads(json_structure["formData"][f"text${text_row['lang']}"].replace("'", '"'))
        json_text['display_text'] = text_row['text']
        child_list = []
        for child, option in zip(text.get('children')[0].get('rows'), json_text['action'].get('options', [])):
            option_copy = deepcopy(option)
            option_copy['display_label'] = child['text']
            child_list.append(option_copy)
        if len(child_list) != 0:
            json_text['action']['options'] = child_list
        json_structure['formData'][f'text${text_row["lang"]}'] = json.dumps(json_text)
        return json_structure

    def _set_bot_lang(self, lang):
        bot_configs = json.loads(self._read_file('app/work_data/tmp/bot.config.json'))
        bot_configs["defaultLanguage"] = lang
        bot_configs["languages"] = [lang]
        self._rewrite_json_file('app/work_data/tmp/bot.config.json', bot_configs)



