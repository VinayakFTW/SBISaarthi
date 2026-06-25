import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()
 
client = MongoClient(os.getenv("MONGO_CONNECTION_STRING"))
db = client['sbi_saarthi']
session_collection = db['sessions']

def get_session(session_id: str):
    # {"_id": 0} as the projection to exclude the ObjectId field
    return session_collection.find_one({"session_id": session_id},{"_id": 0})

def update_session(session_id: str, data: dict):
    session_collection.update_one(
        {"session_id": session_id},
        {"$set": data},
        upsert=True
    )

def clear_session(session_id: str):
    session_collection.delete_one({"session_id": session_id})

def delete_sessions_for_customers(customer_ids: list):
    session_collection.delete_many({"customer_id": {"$in": customer_ids}})

def get_active_session_for_customer(customer_id: int):
    return session_collection.find_one(
        {"customer_id": customer_id},
        {"_id": 0},
        sort=[("last_interaction_at", -1)]
    )
