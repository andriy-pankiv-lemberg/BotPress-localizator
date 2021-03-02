import json

from app.readers.base_reader import BaseReader


class TextReader(BaseReader):

    def __init__(self, bot_id):
        super(TextReader, self).__init__()
        self._bot_id = bot_id

    def read(self):
        texts = self._read_texts()
        for text in texts:
            text_json = json.loads(text.get('text').replace("'", '"'))
            text['text'] = text_json.get('display_text')
            text_id = self._create_text(text, self._bot_id, self._lang)
            self._create_variations(self._cast2variations(text_json), text_id)

    def _read_texts(self):
        texts = self._read_file(f'app/work_data/bots/{self._bot_id}/content-elements/builtin_text.json')
        json_texts = json.loads(texts)
        texts_copy = []
        self._set_language(json_texts, self._bot_id)
        for text in json_texts:
            text_base = {
                'id': text.get('id')
            }
            form_data = text.get('formData')
            text_base['text'] = form_data.get(f'text${self._lang}')
            text_base['schema'] = json.dumps(text)
            text_base['variations'] = self._process_variations(form_data.get(f'variations${self._lang}', []))
            texts_copy.append(text_base)
        return texts_copy

    def _create_variations(self, variations, text_id):
        for variation in variations:
            self._create_variation(variation, text_id, self._lang)

    @staticmethod
    def _cast2variations(text_json):
        action = text_json.get('action')
        if action is None:
            return []
        variations = []
        for option in action.get('options', []):
            variations.append({'text': option.get('display_label')})
        return variations

    @staticmethod
    def _process_variations(variations):
        return [
            {
                'text': variation

            } for variation in variations]
