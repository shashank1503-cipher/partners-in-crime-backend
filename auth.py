from typing import Union
from fastapi import  Header, APIRouter, Request
from google.oauth2 import id_token
from google.auth.transport import requests
from pydantic import BaseModel
import json

router = APIRouter()

def verify(authorization):
    auth_token = authorization.split(" ")[1]
    auth_token = None
    try:
        user = id_token.verify_oauth2_token(auth_token,requests.Request(),  '712712296189-2oahq4t0sis03q14jqoccs8e6tuvpbfd.apps.googleusercontent.com', clock_skew_in_seconds=10)
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

    