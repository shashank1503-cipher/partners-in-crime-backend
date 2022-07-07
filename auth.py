import os
from fastapi import  APIRouter, Request
import firebase_admin
from firebase_admin import auth, credentials
import json
from db import db, read_one, create

router = APIRouter()
FIREBASE_PROJECT_ID = os.environ.get('FIREBASE_PROJECT_ID')
FIREBASE_PRIVATE_KEY_ID = os.environ.get('FIREBASE_PRIVATE_KEY_ID')
FIREBASE_PRIVATE_KEY = os.environ.get('FIREBASE_PRIVATE_KEY')
CLIENT_EMAIL = os.environ.get('CLIENT_EMAIL')
FIREBASE_CLIENT_ID = os.environ.get('FIREBASE_CLIENT_ID')
print(FIREBASE_PRIVATE_KEY)
cred_json = {
   "type": "service_account",
  "project_id": "partners-in-crime-38309",
  "private_key_id": "52f5da41441db64a0da0e99f14a3e880f29aa68e",
  "private_key": "-----BEGIN PRIVATE KEY-----\nMIIEvAIBADANBgkqhkiG9w0BAQEFAASCBKYwggSiAgEAAoIBAQCJ1sjPvax+e99d\n4vFAkGDgfZWlSxm3zeUxj2bUZvlFqgcIkYrfOdM46/k4FELbdwa5wJFH4TEykPMx\nw8P+9vtIUpIkHXYPXLkUi4IfUS4+Wdr6WcsU4PSu2rVu5qGpdIxxRsMWPx32A4c4\nXBgX2ZGsIthUOYTczQNdMFsiqMk4Vk7x5aeQ/w9vmK4lZBsvLxXQ4WNDbY9alq1y\nAMf+YyG3MKz2JxrKR8nfZqJ71uLNi+UoSipAMRfjc7j56+C1RH1tQk7HYjre2hwK\n4oSluj029d+Bjvm9F05WjyrDCzwdjTrxTAGwQ77drBtojJh5M5xwfqQ8HRiENd/j\neoK2K09xAgMBAAECggEAALmGqDD1ZFu1zO//YUuFm3GyKXBR7kvAjL0DtNIu7DCO\n8zG52J8u7Iv6NlL7zdy8DyzRKQOWqXzT5e+n2LkLtb9ZZDYTcWby1HOuLlGvhSD5\nh3rd85644XlTwuDwHl7SgH8b5AvEVkY4wqOrmnkRzLebU5F3kMrFcArZnYfkgl/i\nGvq8OIolM3RgGtTn17WZvvLHJwVLZDM4gYME3uJxbY8s69XXM4RINMPHlwzQRFKS\n6dRGk83izIWpiOkbWt7SUgVIHXXgNuSnidC7Aa8gznnO6oMWNhqVsAgN3vlvhGok\n+qos1N9OWmkYj7DesPp0UcPCrTgzpUq9BI5X+m9AAQKBgQC8YMlrg0IYI4crxB1e\nBPXpSHepRpRw4CePETAkh8OcXHvrFz1DT+T+yAeryRfT4R7c+5s8+gwH51eK1UT4\nnYUj0NRUL9kOehCsD21G8rr2q5/ZBcJPWmiTwDIX2Aqgz4BsOlnT94m7GVdt8mbw\nM20ZHU9+ARA3uO1eE33GFq2scQKBgQC7Uac65OwSIN4K0rpZyg2jbAEAZjo+6CX/\nREyIk5PTd/nQMOvUxX1SKukZ9KzixqdWamuL/noo8SdjbCKtGRoqtcX4jf2HGWvt\n7176hohAQhHpzRj4d1F77xKjj2Q4ta2F8ONE7h3u9mllIQYrW2zRs+u+VqFADknD\nSrr1yGVTAQKBgA3DNHP6XvXMgq+b4FliG2UzuipP0cB9X+Z/5viEQrJFv3fpdrxY\nNe63RngydN8x70NNzoWh7wcUy7yE4EkZmQSI2TpdVIpOOLGZXu50BVzIJSGB3jRV\n8pX40LAVRJGDF2rQyIdH6nQU4eJSd1rNJwdSsOAPy9OGWzEoU2QJfB7BAoGAIDEt\nO0riY08wuc1zZ0D5TQ+fsHDhK7R76z3SpVovepVQ4n212fBC1F85hlNtbt/THF/X\nscx/NBAVw9lusC7zN0ncBxZn7tLooJCV0xpRyjFQoMy1sOXYpCL3IhLfl3tpoe4/\nMLZ3gHzqqg2d4M+qiPOR3TlIJxkNhjmOnfTdrQECgYAPbCEDLOyIJZObl2hzva2z\nND8yrxUmItkCgDltDZep9ilW5aH8NQMyEbdvpK2MDw1+xpcrByfIfkBbx7JCVOTj\n9Umv5967v6DUpRoygP/u3y52yWY7nm2ffFs0B+xuRb75CCmz+vpSLEFGsQ0Q9FGS\nIBkOJwJYYGASro96xPOb6Q==\n-----END PRIVATE KEY-----\n",
  "client_email": "firebase-adminsdk-q3sfa@partners-in-crime-38309.iam.gserviceaccount.com",
  "client_id": "101763737847514038361",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "https://www.googleapis.com/robot/v1/metadata/x509/firebase-adminsdk-q3sfa%40partners-in-crime-38309.iam.gserviceaccount.com"
}
cred = credentials.Certificate(cred_json)
firebase_admin.initialize_app(cred)

async def verify(authorization):
   
    # print(authorization)
    try:
        id_token = authorization.split(" ")[1]
        # print(auth_token)
        # user = id_token.verify_oauth2_token(auth_token,requests.Request(),  '712712296189-2oahq4t0sis03q14jqoccs8e6tuvpbfd.apps.googleusercontent.com', clock_skew_in_seconds=10)
        user = auth.verify_id_token(id_token)
        
        # print("---------------------------------------")
        # print("USER : ", user)
        # print("---------------------------------------")
        
        return user
    except Exception as e:
        print(e)
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

    if verify(req.headers["authorization"]):
        print("YES")
    else:
        return {"error": "Not Authorized"}

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
