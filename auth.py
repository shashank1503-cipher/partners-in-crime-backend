from typing import Union
from fastapi import  Header, APIRouter, Request
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel
import json
from db import db, read_one, create

router = APIRouter()

def verify(authorization):
    auth_token = authorization.split(" ")[1]
    try:
        user = id_token.verify_oauth2_token(auth_token,requests.Request(),  '712712296189-2oahq4t0sis03q14jqoccs8e6tuvpbfd.apps.googleusercontent.com', clock_skew_in_seconds=10)
        # print(user)
        return True
    except:
        return False



@router.post('/auth/adduser')
async def addUser(req: Request):

    if verify(req.headers["authorization"]):
        print("YES")
    else:
        return {"error": "Not Authorized"}

    data = await req.body()
    data = json.loads(data)
    data = data['user']

    new_data = checkIfUserExists(data['g_id'])
    # print("Data 2: ", data)
    if not new_data:
        addUser(data)
        return {
            "message":"Added User",
            "code": 1
        }
    else:
        return {
            "data": data,
            "code": 2
        }


def checkIfUserExists(id):
    data = read_one(db, 'users', {'g_id':f'{id}'})

    if not data:
        return None
    
    return data

    
def addUser(data):
   
    try:
        create(db, 'users', data)
    except:
        return {"error": "error adding user."}


@router.post('/auth/getUser')
async def getdata(req: Request):
    data = await req.body()
    id = json.loads(data)['g_id']
    print(id)


    user = checkIfUserExists(id)
    print(user)

    if not user:
        return {'error': 'error'}

    return {"user": {
        "name": user['name'],
        "email": user['email'],
        'photo': user['photo'],
        'g_id': user['g_id']
    }}