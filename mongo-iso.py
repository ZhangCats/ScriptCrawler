#from pymongo import MongoClient
import pymongo
import dateutil
import dateutil.parser
import time
from datetime import datetime

MONGO_URI = 'mongodb://127.0.0.1:27017'
MONGO_DATABASE = 'Mongo'
MONGO_COLLECTION = 'ceshi'

client = pymongo.MongoClient(MONGO_URI)
db = client[MONGO_DATABASE]
collection = db[MONGO_COLLECTION]
collection.create_index([("deletetime", pymongo.ASCENDING)], expireAfterSeconds=120)


timeStamp = 1527584700
timeArray = time.localtime(timeStamp)
dateStr = time.strftime("%Y-%m-%dT%H:%M:%SZ", timeArray)
#dateStr = '2018-05-29T08:25:00Z'
myDatetime = dateutil.parser.parse(dateStr)

data = {
   "one": 2,
   "two": 235,
   "three": "hello world",
   #"deletetime": datetime.now(),
   "deletetime": myDatetime,
   "time": datetime.utcnow(),
}
collection.insert(data)


