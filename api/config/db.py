from pymongo import MongoClient
from api.config.settings import Settings

settings = Settings()

MongoClient = MongoClient(settings.mongo_url)
db = MongoClient.UserData
