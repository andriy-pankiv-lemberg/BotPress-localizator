import json

from app.readers.base_reader import BaseReader


class SingleChoiceReader(BaseReader):

    def __init__(self, bot_id):
        super(SingleChoiceReader, self).__init__()
        self._bot_id = bot_id

    def read(self):
        single_choices = self._read_single_choices()
        for single_choice in single_choices:
            single_choice_id = self._create_single_choice(single_choice, self._bot_id, self._lang)
            self._create_choices(single_choice.get('choices'), single_choice_id)

    def _read_single_choices(self):
        single_choices = self._read_file(f'app/work_data/bots/{self._bot_id}/content-elements/builtin_single-choice.json')
        json_single_choices = json.loads(single_choices)

        single_choices_copy = []
        self._set_language(json_single_choices, self._bot_id)
        for single_choice in json_single_choices:
            single_choice_base = {
                'id': single_choice.get('id')
            }
            form_data = single_choice.get('formData')
            single_choice_base['text'] = form_data.get(f'text${self._lang}')
            single_choice_base['schema'] = json.dumps(single_choice)
            single_choice_base['choices'] = self._process_choices(form_data.get(f'choices${self._lang}'))
            single_choices_copy.append(single_choice_base)
        return single_choices_copy

    def _create_choices(self, actions, single_choice_id):
        for action in actions:
            self._create_choice(action, single_choice_id)

    @staticmethod
    def _process_choices(choices):
        return [
            {
                'title': choice.get('title')

            } for choice in choices]
