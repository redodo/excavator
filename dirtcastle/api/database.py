from pymongo import MongoClient

from . import settings


client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_NAME]


def init_db(db):
    # create globals
    if not db.globals.find_one({'key': 'tokens'}):
        db.globals.insert_one({'key': 'tokens', 'value': {}})
