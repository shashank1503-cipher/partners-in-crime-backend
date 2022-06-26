import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://partnersInCrime:partners123@cluster0.grt0lph.mongodb.net/?retryWrites=true&w=majority")
db = client["partnersInCrime"]

def read(db, collection, query):
    return db[collection].find(query)
def read_one(db, collection, query):
    return db[collection].find_one(query)
def create(db, collection, data):
    return db[collection].insert_one(data)
def update(db, collection, query, data):
    return db[collection].update_one(query, data)
def delete(db, collection, query):
    return db[collection].delete_one(query)
