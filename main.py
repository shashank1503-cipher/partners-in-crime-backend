from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import auth

# from .db import read, read_one, create, update, delete 


app = FastAPI()

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)

@app.get("/")
def home():
    return {"Let's": "Go"}
