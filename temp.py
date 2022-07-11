import pymongo

from db import MONGO_URI

# MONGO_URI = os.environ.get('MONGO_URI')
MONGO_URI = 'mongodb+srv://partnersInCrime:partners123@cluster0.grt0lph.mongodb.net/?retryWrites=true&w=majority'
client = pymongo.MongoClient(MONGO_URI)

skills = client["partnersInCrime"]["skills"]
fetch_skills = skills.find()

for skill in fetch_skills:
    count_dup = skills.count_documents({'name': skill['name']})
    if count_dup > 1:
        skills.delete_one({'name': skill['name']})
        print(f'{skill["name"]} deleted')