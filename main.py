from fastapi import FastAPI

# from .db import read, read_one, create, update, delete 

app = FastAPI()

@app.get("/")
def home():
    return {"Let's": "Go"}
