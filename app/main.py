from typing import Union
from fastapi import FastAPI, HTTPException
from pymongo.mongo_client import MongoClient
import os

app = FastAPI()

uri = os.environ.get("MONGO_URI")
client = MongoClient(uri)
try:
    client.admin.command("ping")
    print("Pinged Your Deployment, You Successfully Connected to MongoDB")
except Exception as e:
    raise HTTPException(status_code=500, detail="Database connection error")


@app.get("/")
async def read_root() -> Union[str, dict]:
    return {"Hello": "World"}
