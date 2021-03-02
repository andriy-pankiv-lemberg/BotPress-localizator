import csv

from app.builder.base_builder import BaseBuilder


class CsvBuilder(BaseBuilder):

    def __init__(self, bot_id, translate_languages=None):
        super(CsvBuilder, self).__init__(bot_id)
        self._translate_languages = translate_languages or []

    def build(self):
        bot = self._get_bot()
        self._generate_csv(bot)

    def _generate_csv(self, bot):
        path = f'app/work_data/out/csv/{self._remove_extension(bot.get("file_name"))}-{self._bot_id}.csv'
        with open(path, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(["id", bot.get("lang")] + self._translate_languages)
            for phrase in bot.get('phrases'):
                row = [phrase.get('id'), phrase.get('text')] + [' ' for _ in range(len(self._translate_languages))]
                writer.writerow(row)


