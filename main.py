import json
import pymongo
from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from bson import ObjectId
import auth


# from .db import read, read_one, create, update, delete 
from fastapi.middleware.cors import CORSMiddleware

from auth import verify
from utils import check_user_exists_using_email
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
        data.append({"name":i["name"]})
        subskills = i.get("subskills", [])
        for j in subskills:
            if j:
                count+=1
                data.append({"name":j})
    result["meta"]={"total":count}
    result["data"]=data

    return result

@app.post("/addproject")
async def add_project(req: Request):
  
  user = verify(req.headers.get("Authorization"))
  
  if not user:
    raise HTTPException(status_code=401, detail="Unauthorized")
  user_email = user.get("email", None)
  if not user_email:
    raise HTTPException(status_code=400, detail="User Email Not Found")
  fetch_user = check_user_exists_using_email(user_email)
  if not fetch_user:
    raise HTTPException(status_code=400, detail="User Not Found")
  result = {}

  result['name'] = fetch_user.get("name", None)
  result['email'] = fetch_user.get("email", None)
  result ['image'] = fetch_user.get("photo", None)  
  data = await req.body()
  if data:
    data = json.loads(data)
  result['hero_image'] = data.get("image_url", None)
  result['title'] = data.get("title", None)
  result['idea'] = data.get("idea", None)
  result['required_skills'] = data.get("skills", None)
  try:
    collection = db["projects"]
    fetch_inserted_project = collection.insert_one(result)
    fid = str(fetch_inserted_project.inserted_id)
    result.pop("_id")
    return {"meta":{"inserted_id":fid},"data":result}
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail="Error Adding Project")
  
@app.get('/notifications')
def get_notifications(req: Request,page:int=1,per_page:int=10):
  # user = verify(req.headers.get("Authorization"))
  # if not user:
  #   raise HTTPException(status_code=401, detail="Unauthorized")
  # user_email = user.get("email", None)
  user_email = "shashankkumar20bcs15@iiitkottayam.ac.in"

  if not user_email:
    raise HTTPException(status_code=400, detail="User Email Not Found")
  fetch_user = check_user_exists_using_email(user_email)
  if not fetch_user:
    raise HTTPException(status_code=400, detail="User Not Found")
  user_id = fetch_user.get("_id", None)
  fetch_notifications = db["notifications"].find({"user_id":user_id}).sort("created_at",-1).skip((page-1)*per_page).limit(per_page)
  fetch_count = db["notifications"].count_documents({"user_id":user_id})
  if not fetch_notifications:
    raise HTTPException(status_code=404, detail="No Notifications Found")
  result = {'new':[],'read':[]}
  for i in list(fetch_notifications):
    i['_id'] = str(i['_id'])
    i['user_id'] = str(i['user_id'])
    created_at = i.pop("created_at")
    i['date'] = created_at.strftime("%d %b %Y")
    i['time'] = created_at.strftime("%I:%M %p")
    if i['is_read'] == False:
      result['new'].append(i)
    else:
      result['read'].append(i)
  return {'meta':{'total_records':fetch_count,'page':page,'per_page':per_page}, 'data':result}

@app.put('/notifications/{id}')
def update_notification(req: Request,id:str):
  # user = verify(req.headers.get("Authorization"))
  # if not user:
  #   raise HTTPException(status_code=401, detail="Unauthorized")
  # user_email = user.get("email", None)
  user_email = "shashankkumar20bcs15@iiitkottayam.ac.in"
  if not user_email:
    raise HTTPException(status_code=400, detail="User Email Not Found")
  fetch_user = check_user_exists_using_email(user_email)
  if not fetch_user:
    raise HTTPException(status_code=400, detail="User Not Found")
  try:
    db['notifications'].update_one({"_id":ObjectId(id)},{"$set":{"is_read":True}})
    return {"meta":{"status":"success"},"data":{}}
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail="Error Updating Notification")
    
app.include_router(auth.router)


# fetch 
@app.get('/search')
def findkey(req: Request,q):
  count=db.users.count_documents({"name": q})
  cursor = db.users.find({"name": q})
  res={}
  res["meta"]={}
  res["data"]=[]
  for i in list(cursor):
    i["_id"]=str(i["_id"])
    res["data"].append(i)
  res["meta"]={"count":count}
  cursor = db.skills.find_one({"name": q})
  if(cursor):
    main_skill=cursor["name"]
    sub_skills=cursor["subskills"]
    fetch_main_profile=db.users.find({"skills":{"$regex":main_skill,"$options":"i"}})
    for i in list(fetch_main_profile):
      i["_id"]=str(i["_id"])
      res["data"].append(i)
    for sub_skill in sub_skills:
      fetch_sub_profile=db.users.find({"skills":{"$regex":sub_skill,"$options":"i"}})
      for i in list(fetch_sub_profile):
        i["_id"]=str(i["_id"])
        res["data"].append(i) 
  else:
    fetch_query=db.users.find({"skills":{"$regex":q,"$options":"i"}})
    for i in list(fetch_query):
      i["_id"]=str(i["_id"])
      res["data"].append(i)
    res["meta"]={"count":count}
  return res


@app.post("/addfavourite")
async def add_favourite(req: Request):
  # user = verify(req.headers.get("Authorization"))
  # if not user:
  #   raise HTTPException(status_code=401, detail="Unauthorized")
  # user_email = user.get("email", None)
  # if not user_email:
  #   raise HTTPException(status_code=400, detail="User Email Not Found")
  user_email = "shashankkumar20bcs15@iiitkottayam.ac.in"
  fetch_user = check_user_exists_using_email(user_email)
  if not fetch_user:
    raise HTTPException(status_code=400, detail="User Not Found")
  result = {}
  data = await req.body()
  if data:
    data = json.loads(data)
  result['user_id'] = fetch_user.get("_id", None)
  result['hackathon_id'] = data.get("hackathon_id", None)
  result['project_id'] = data.get("project_id", None)
  try:
    collection = db["favourites"]
    fetch_inserted_project = collection.insert_one(result)
    fid = str(fetch_inserted_project.inserted_id)
    result.pop("_id")
    result.pop("user_id")
    return {"meta":{"inserted_id":fid},"data":result}
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail="Error Adding Favourite")
@app.delete('/deleteFavourite/{id}')
async def delete_favourite(req: Request,id:str,is_project:bool=False):
  # user = verify(req.headers.get("Authorization"))
  # if not user:
  #   raise HTTPException(status_code=401, detail="Unauthorized")
  # user_email = user.get("email", None)
  # if not user_email:
  #   raise HTTPException(status_code=400, detail="User Email Not Found")
  user_email = "shashankkumar20bcs15@iiitkottayam.ac.in"
  fetch_user = check_user_exists_using_email(user_email)
  if not fetch_user:
    raise HTTPException(status_code=400, detail="User Not Found")
  query = {}
  query['user_id'] = fetch_user.get("_id", None)
  if is_project:
    query['project_id'] = id
  else:
    query['hackathon_id'] = id  
  try:
    collection = db["favourites"]
    collection.delete_one(query)
    return {"meta":{"status":"success"},"data":{}}
  except Exception as e:
    print(e)
    raise HTTPException(status_code=500, detail="Error Adding Favourite")
@app.get("/fetchprojects")

@app.get("/")
def home():
    return {"Let's": "Go"}
