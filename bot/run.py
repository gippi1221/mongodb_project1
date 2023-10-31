import asyncio
import logging
import sys
import os
import json

from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

from aiogram import Bot, Dispatcher, types
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram.utils.markdown import hbold

from db_service import MongoDBService

token = os.getenv('TG_TOKEN')
db_url = os.getenv('DB_CONN')
db_name = os.getenv('DB_NAME')

dp = Dispatcher()

def get_ranges(dt_1, dt_2, group_type):
  date_range = []

  if group_type == "hour":
    interval = timedelta(hours=1)
  elif group_type == "day":
    interval = timedelta(days=1)
  elif group_type == "week":
      interval = timedelta(weeks=1)
  elif group_type == "month":
    interval = relativedelta(months=1)
  else:
    raise ValueError("Invalid group_type. Supported group_type are 'hour', 'day', 'week' or 'month'.")

  current_date = dt_1
  while current_date <= dt_2:
    date_range.append(current_date)
    current_date += interval
  
  return date_range

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
  await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")


@dp.message()
async def process_input(message: types.Message) -> None:

  input_data = json.loads(message.text)

  try:
    
    dt_1 = datetime.strptime(input_data['dt_from'], '%Y-%m-%dT%H:%M:%S')
    dt_2 = datetime.strptime(input_data['dt_upto'], '%Y-%m-%dT%H:%M:%S')
    dt_type = input_data['group_type']

    ranges = get_ranges(dt_1, dt_2, dt_type)

    db_service = MongoDBService(db_url, db_name)

    result = await db_service.run_aggregation(dt_1, dt_2, dt_type)
    
    db_service.close_connection()

    dataset = result['dataset']
    labels = result['labels']

    new_ds = []
    new_labels = []
    
    for idx, x in enumerate(ranges):
      new_labels.append(datetime.strftime(x, '%Y-%m-%dT%H:%M:%S'))
      if x in labels:
        index = labels.index(x)
        new_ds.append(dataset[index])
      else:
        new_ds.append(0)

    output_data = {
      'dataset': new_ds,
      'labels': new_labels
    }

    result_json = json.dumps(output_data, default=str)

    await message.answer(result_json)
  except Exception as e:
    await message.answer("An error occurred: {}".format(str(e)))


async def main() -> None:
  bot = Bot(token, parse_mode=ParseMode.HTML)
  await dp.start_polling(bot)


if __name__ == "__main__":
  logging.basicConfig(level=logging.INFO, stream=sys.stdout)
  asyncio.run(main())