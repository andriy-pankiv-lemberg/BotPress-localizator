import json


def main():
    with open('work_data/content-elements/builtin_card_TEST.json') as f:
        cards = f.read()
    json_cards = json.loads(cards)
    print(cards)
    cards_copy = []
    template_language = get_language(json_cards)
    json_cards = json.loads(clear_file(cards, template_language))
    for card in json_cards:
        card_base = {
            'id': card.get('id')
        }
        form_data = card.get('formData')
        card_base['title'] = form_data.get('title')
        card_base['actions'] = process_actions(form_data.get('actions'))
        cards_copy.append(card_base)
    print(cards_copy)



def process_actions(actions):
    return [
        {
            'title': action.get('title'),

        } for action in actions
    ]



def get_language(cards):
    first_card = cards[0]
    form_data = first_card.get('formData')
    return list(form_data.keys())[0].split('$')[1]


def clear_file(file_text, lang):
    return file_text.replace(f'${lang}', '')



if __name__ == '__main__':
    main()
