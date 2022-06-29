from typing import Union
from fastapi import  Header, APIRouter
from google.oauth2 import id_token
from google.auth.transport import requests

router = APIRouter()

@router.get('/auth/verify')
def verify(authorization: Union[str, None] = Header(default=None)):
    auth_token = authorization.split(" ")[1]
    print(auth_token)
    user = id_token.verify_oauth2_token(auth_token,requests.Request(),  '712712296189-2oahq4t0sis03q14jqoccs8e6tuvpbfd.apps.googleusercontent.com', clock_skew_in_seconds=10)
    print(user)
    return user

