from app.readers import BotReader, CsvReader
from app.builder import CsvBuilder, BotBuilder


def main():
    bot_reader = BotReader(file_name)
    bot_id = bot_reader.read()
    csv_builder = CsvBuilder(bot_id, ['en'])
    csv_builder.build()
    csv_reader = CsvReader(csv_file)
    new_bots = csv_reader.read()
    first_bot = new_bots[0]
    bot_builder = BotBuilder(first_bot.get('id'))
    bot_builder.build(f'new_bot-{first_bot.get("lang")}.tgz')


if __name__ == "__main__":
    main()
