from pymongo import MongoClient

from . import settings


client = MongoClient(settings.MONGO_HOST, settings.MONGO_PORT)
db = client[settings.MONGO_NAME]
