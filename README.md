# BotPress-localizator
Python module to help translate BotPress bot

# How to use

## Read bot
Firstly, add your `.tgz` bot file to `app/work_data/in/bots/`. After that, you can start reading your bot into DB.

Example
```python
from app.readers import BotReader
file_name = 'nela-bot.tgz'
bot_reader = BotReader(file_name)
bot_id = bot_reader.read()
```
where `bot_id` ID of a bot in `TranslateDB`

## Create CSV
All you need, is to now `bot_id` and **list of languages** to translate with. After that, you can start creating your csv from DB.

Example
```python
from app.builder import CsvBuilder
bot_id = 1
csv_builder = CsvBuilder(bot_id, ['fr', 'ua'])
csv_name = csv_builder.build()
```
where `csv_name` is name of generated file in `app/work_data/out/csv/` folder.

## Read CSV
To read translated CSV(from previous step), you need to add edited .csv file to `app/work_data/in/csv/` folder. After that, you can start reading your csv into DB.

```python
from app.readers import CsvReader
csv_file = 'translated-bot.csv'
csv_reader = CsvReader(csv_file)
new_bots = csv_reader.read()
```
where `new_bots` is a list of the new bots info
```json
[
  {
    "id": 2,
    "lang": "fr"
  },
  {
    "id": 3,
    "lang": "en"
  }
]
```

## Build bot
All you need, is to have `bot_id` of the bot you need to build, as well as, name of a `.tgz` file(**with extension**)

Example
```python
from app.builder import BotBuilder
bot_id = 1
bot_builder = BotBuilder(bot_id)
bot_builder.build(f'new_bot-{bot_id}.tgz')
```
you will find your bot `.tgz` file in `app/work_data/out/bots/`