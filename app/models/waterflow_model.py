from app.utils.db_utils import get_client, get_collection
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from flask import session
from typing import Optional, Dict, Any
from utils import generate_token
import pytz

class Waterflow_model:
    def __init__(self) -> None:
        self._client: Optional[MongoClient] = None
        self._waterflow_collection: Optional[Collection] = None
        self._user_collection: Optional[Collection] = None
    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = get_client()
        return self._client
    
    @property
    def waterflow_collection(self) -> Collection:
        if self._waterflow_collection is None:
            self._waterflow_collection = get_collection("waterflows")
        return self._waterflow_collection
    
    @property
    def users_collection(self) -> Collection:
        if self._user_collection is None:
            self._user_collection = get_collection("users")
        return self._user_collection

    def generate_token_to_user(self, user_id): 
        db = self.users_collection

        token = generate_token()
        
        try:
            db.update_one(
                {"_id": ObjectId(user_id)},
                {"$set": {"token": token}}
            )
            return True
        except:
            return False
        
    def send_command_to_change(self, mac_address, activate: bool):
        db = self.waterflow_collection
        local_zone = pytz.timezone('America/Chihuahua')
        local_date = datetime.now(local_zone)
        try:
            db.update_one(
                {"_id": ObjectId(mac_address)},
                {"$set": {"activate": activate},
                 "$push": {"history": local_date}},
                )
            return True
        except:
            return False
        
    def get_waterflow_state_db(self, mac_address):
        db = self.waterflow_collection

        state = db.find_one({"_id": ObjectId(mac_address)}, {"activate": 1, "_id": 0})
        
        return state
    
    def send_token_from_waterflow(self, token, mac_address):
        db_waterflow = self.waterflow_collection

        db_users = self.users_collection

        try:
            db_users.update_one(
                {"token": token},
                {"$push": {"waterflows": ObjectId(mac_address)}}
            ) 

            query = {
                "_id": ObjectId(mac_address),
                "activate": False,
                "history": []
            }

            db_waterflow.insert_one(query)

            return True
        except:
            return False

    def waterflow_in_database(self, mac_address):
        db = self.waterflow_collection

        waterflow = db.find_one({"_id": ObjectId(mac_address)})

        if waterflow:
            return True
        
        return False
    
    def get_waterflows_user(self, user_id):
        user = self.users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "waterflows": 1})
        return user["waterflows"] if user else None
    
    def get_history_of_the_waterflow(self, mac_address):
        db = self.waterflow_collection
        waterflow = db.find_one({"_id": ObjectId(mac_address)}, {"_id": 0, "history": 1})
        return waterflow["history"] if waterflow else None
    
    def get_information_waterflows(self, user_id):
        wf_ids = self.get_waterflows_user(user_id)
        if not wf_ids:
            return None
        
        try:
            object_ids = [ObjectId(wf) for wf in wf_ids]
        except Exception:
            return None

        cursor = self.waterflow_collection.find(
            {"_id": {"$in": object_ids}},
            {"waterflow_mac": 1, "activate": 1, "history": 1}
        )

        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])
            raw_history = doc.get("history", [])
            doc["history"] = [
                dt.isoformat() if hasattr(dt, "isoformat") else str(dt)
                for dt in raw_history
            ]
            results.append(doc)

        return results


model_waterflow = Waterflow_model()