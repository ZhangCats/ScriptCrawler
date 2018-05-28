#from pymongo import MongoClient
import pymongo
#import datetime
from datetime import datetime
MONGO_URI = 'mongodb://127.0.0.1:27017'
MONGO_DATABASE = 'Mongo'
MONGO_COLLECTION = 'ceshi'

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]
collection.create_index([("time", pymongo.ASCENDING)], expireAfterSeconds=60*60*1*1)

data = {
   "one": 1,
   "two": 235,
   "three": "hello world",
   "time": datetime.utcnow(),
}
collection.insert(data)
