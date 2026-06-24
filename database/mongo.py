import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017/")
client = MongoClient(MONGO_URI)
db = client['sbi_saarthi']
session_collection = db['sessions']

def get_session(session_id: str):
    return session_collection.find_one({"session_id": session_id})

def update_session(session_id: str, data: dict):
    session_collection.update_one(
        {"session_id": session_id},
        {"$set": data},
        upsert=True
    )
