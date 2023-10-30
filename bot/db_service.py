import pymongo
import asyncio
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

class MongoDBService:

  def __init__(self, db_url, db_name):
    self.client = pymongo.MongoClient(db_url)
    self.db = self.client[db_name]

  def close_connection(self):
    self.client.close()

  async def run_aggregation(self, dt_1, dt_2, dt_type):

    date_range = {
        "$gte": dt_1,
        "$lte": dt_2
    }

    date_trunc_unit = dt_type

    pipeline = [
        {
            "$match": {
                "dt": date_range
            }
        },
        {
            "$group": {
                "_id": { "$dateTrunc": { "date": "$dt", "unit": date_trunc_unit } },
                "total_sum": { "$sum": "$value" }
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        },
        {
            "$group": {
                "_id": None,
                "labels": { "$push": "$_id" },
                "dataset": { "$push": "$total_sum" }
            }
        },
        {
            "$project": {
                "_id": 0,
            }
        }
    ]

    result = self.db.sample_collection.aggregate(pipeline).next()
    return result


  async def run_aggregation_details(self, dt_1, dt_2, dt_type):

    date_range = {
        "$gte": dt_1,
        "$lte": dt_2
    }

    date_trunc_unit = dt_type

    pipeline = [
        {
            "$match": {
                "dt": date_range
            }
        },
        {
            "$group": {
                "_id": { "$dateTrunc": { "date": "$dt", "unit": date_trunc_unit } },
                "total_sum": { "$sum": "$value" }
            }
        },
        {
            "$sort": {
                "_id": 1
            }
        },
    ]

    result = list(self.db.sample_collection.aggregate(pipeline))
    return result