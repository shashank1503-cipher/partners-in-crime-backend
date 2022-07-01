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
        print(user)
        return user
    except:
        return False
    


