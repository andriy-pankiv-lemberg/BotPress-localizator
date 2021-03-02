import json

from app.readers.base_reader import BaseReader


class CardReader(BaseReader):

    def __init__(self, bot_id):
        super(CardReader, self).__init__()
        self._bot_id = bot_id

    def read(self):
        cards = self._read_cards()
        for card in cards:
            card_id = self._create_card(card, self._bot_id, self._lang)
            self._create_actions(card.get('actions'), card_id)

    def _read_cards(self):
        cards = self._read_file(f'app/work_data/bots/{self._bot_id}/content-elements/builtin_card.json')
        json_cards = json.loads(cards)
        cards_copy = []
        self._set_language(json_cards, self._bot_id)
        for card in json_cards:
            card_base = {
                'id': card.get('id')
            }
            form_data = card.get('formData')
            card_base['title'] = form_data.get(f'title${self._lang}')
            card_base['schema'] = json.dumps(card)
            card_base['subtitle'] = form_data.get(f'subtitle${self._lang}')
            card_base['actions'] = self._process_actions(form_data.get(f'actions${self._lang}'))
            cards_copy.append(card_base)
        return cards_copy

    @staticmethod
    def _process_actions(actions):
        return [
            {
                'title': action.get('title')

            } for action in actions]
