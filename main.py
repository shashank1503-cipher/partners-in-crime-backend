from typing import Collection
import pymongo
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
#import auth

# from .db import read, read_one, create, update, delete 
from fastapi.middleware.cors import CORSMiddleware
client = pymongo.MongoClient("mongodb+srv://partnersInCrime:partners123@cluster0.grt0lph.mongodb.net/?retryWrites=true&w=majority")
db = client["partnersInCrime"]
app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
@app.get("/suggestions")
def autocomp(q):
    pipeline = [
   {
     '$search': {
       'index': 'autodefault',
       "autocomplete": {
         "query": q,
         "path":'name',
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
    skillCollection = db['skills']
    pipeline[-1] = {
     '$project': {
       "name": 1,
        "subskills": 1
     }
   }
   
    aggregatedresult=skillCollection.aggregate(pipeline)
    for i in list(aggregatedresult):
        count+=1
        data.append({"name":i["name"] + " " + "Developer"})
        subskills = i.get("subskills", [])
        for j in subskills:
            if j:
                count+=1
                data.append({"name":j + " " + "Developer"})
    result["meta"]={"total":count}
    result["data"]=data

    return result

#app.include_router(auth.router)

@app.get("/")
def home():
    return {"Let's": "Go"}

if __name__ == '__main__':
    uvicorn.run(app, port=8000)