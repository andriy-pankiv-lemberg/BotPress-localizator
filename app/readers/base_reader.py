import tarfile

from app.base import Base


class BaseReader(Base):

    def __init__(self):
        super(BaseReader, self).__init__()
        self._lang = None
        self._file_name = None
        self._readers = {
            'card': {
                'table_name': 'cards',
                'class': 'CardReader'
            },
            'single-choice': {
                'table_name': 'single_choices',
                'class': 'SingleChoiceReader'
            },
            'text': {
                'table_name': 'texts',
                'class': 'TextReader'
            }
        }

    def read(self):
        raise NotImplementedError

    def _unzip(self, bot_id):
        path = f'app/work_data/in/bots/{self._file_name}'
        with tarfile.open(path, "r:gz") as tar:
            tar.extractall(path=f'app/work_data/bots/{bot_id}')

    def _create_bot(self, lang=None):
        return self._translate_db.insert('bots',
                                         data={
                                             'file_name': self._file_name,
                                             'lang': lang
                                         }, return_id=True)

    def _set_language(self, cards, bot_id):
        if self._lang is None and len(cards) != 0:
            first_card = cards[0]
            form_data = first_card.get('formData')
            self._lang = list(form_data.keys())[0].split('$')[1]
            self._translate_db.update('bots',
                                      where_statements={'id': bot_id},
                                      data={'lang': self._lang})

    def _create_phrase(self, text, lang):
        return self._translate_db.insert('phrases',
                                         data={
                                             'text': text,
                                             'lang': lang
                                         },
                                         return_id=True)

    def _create_card(self, card, bot_id, lang):
        return self._translate_db.insert('cards',
                                         data={
                                             'phrase_id': self._create_phrase(card.get('title'), lang),
                                             'element_id': card.get('id'),
                                             'title': card.get('title'),
                                             'subtitle': card.get('subtitle'),
                                             'schema': card.get('schema'),
                                             'bot_id': bot_id,
                                             'lang': lang
                                         }, return_id=True)

    def _create_action(self, action, card_id, lang):
        self._translate_db.insert('actions',
                                  data={
                                      'phrase_id': self._create_phrase(action.get('title'), lang),
                                      'card_id': card_id,
                                      'title': action.get('title')
                                  })

    def _create_actions(self, actions, card_id):
        for action in actions:
            self._create_action(action, card_id, self._lang)

    def _create_single_choice(self, single_choice, bot_id, lang):
        return self._translate_db.insert('single_choices',
                                         data={
                                             'phrase_id': self._create_phrase(single_choice.get('text'), self._lang),
                                             'element_id': single_choice.get('id'),
                                             'text': single_choice.get('text'),
                                             'schema': single_choice.get('schema'),
                                             'bot_id': bot_id,
                                             'lang': lang
                                         }, return_id=True)

    def _create_choice(self, action, single_choice_id):
        self._translate_db.insert('choices',
                                  data={
                                      'phrase_id': self._create_phrase(action.get('title'), self._lang),
                                      'single_choice_id': single_choice_id,
                                      'title': action.get('title')
                                  })

    def _create_text(self, text, bot_id, lang):
        return self._translate_db.insert('texts',
                                         data={
                                             'phrase_id': self._create_phrase(text.get('text'), lang),
                                             'element_id': text.get('id'),
                                             'text': text.get('text'),
                                             'schema': text.get('schema'),
                                             'bot_id': bot_id,
                                             'lang': lang
                                         }, return_id=True)

    def _create_variation(self, variation, text_id, lang):
        self._translate_db.insert('variations',
                                  data={
                                      'phrase_id': self._create_phrase(variation.get('text'), lang),
                                      'text_id': text_id,
                                      'text': variation.get('text')
                                  })
