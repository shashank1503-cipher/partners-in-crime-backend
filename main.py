import uvicorn
import pymongo
from bson.objectid import ObjectId

client = pymongo.MongoClient("mongodb+srv://partnersInCrime:partners123@cluster0.grt0lph.mongodb.net/?retryWrites=true&w=majority")
db = client["partnersInCrime"]
from fastapi import FastAPI

#from .db import read, read_one, create, update, delete 

app = FastAPI()
@app.get("/suggestions")
def autocomp(q):
    pipeline = [
   {
     '$search': {
       'index': 'autodefault',
       "autocomplete": {
         "query": q,
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
    count=0

    collections=db["users"]
    aggregatedresult=collections.aggregate(pipeline)
    result={}
    data=[]
    for i in list(aggregatedresult):
        count+=1
        data.append({"name":i["name"]})
    result["meta"]={"total":count}
    result["data"]=data

    return result



@app.get("/")
def home():
    return {"Let's": "Go"}
if __name__ == '__main__':
    uvicorn.run(app, port=8000)