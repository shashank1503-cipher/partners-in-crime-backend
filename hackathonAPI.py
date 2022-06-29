from unittest import result
import pymongo
client = pymongo.MongoClient("mongodb+srv://partnersInCrime:partners123@cluster0.grt0lph.mongodb.net/?retryWrites=true&w=majority")
db = client["partnersInCrime"]

collection = db['users']

pipeline = [
   {
     '$search': {
       'index': 'autodefault',
       "autocomplete": {
         "query": 'aka',
         "path": "name",
         "tokenOrder": "sequential"
       }
     }
   },
   {
     '$limit': 10
   },
   {
     '$project': {
       "name": 1
     }
   }
   
   ]
   

result = []
aggregated = (list(collection.aggregate(pipeline)))
for i in aggregated:
  result.append(i['name'])
print(result)