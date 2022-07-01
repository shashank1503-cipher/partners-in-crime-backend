from datetime import datetime
from db import create, read_one,db
from bson import ObjectId

def check_user_exists_using_email(email):
    user = read_one(db,"users", {"email": email})
    if user:
        return user
    return None
def create_notification(user_id, title,description,type):
    notification = {
        "user_id": user_id,
        "title": title,
        'description': description,
        'type': type,
        'created_at': datetime.now(),
        'is_read': False
    }
    create(db, "notifications", notification)

notification =  [
    {
      'title': 'MLH Hackathon Invitation',
      'description':
        'Bla Bla has invited you to participated in the MLH Hackathon.',
      "type": 'Invitation',
    },
    {
      "title": 'New Message',
      'description': 'Bla Bla has sent you a message',
      "type": 'Message',
    },
  ]

user_id = ObjectId("62be89a9df9fa5b672b8961f")
for i in notification:

    create_notification(user_id, i['title'], i['description'], i['type'])
