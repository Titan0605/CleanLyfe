from app.utils.db_utils import get_client, get_collection
from app.utils import generate_token
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from flask import session
from typing import Optional, Dict, Any
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
            return token
        except:
            return None
        
    def send_command_to_change(self, mac_address, activate: bool):
        db = self.waterflow_collection
        local_zone = pytz.timezone('America/Chihuahua')
        local_date = datetime.now(local_zone)
        try:
            db.update_one(
                {"MAC": mac_address},
                {"$set": {"active": activate},
                 "$push": {"history": {"date": local_date,
                                       "state": activate
                                       }}},
                )
            return True
        except:
            return False
        
    def get_waterflow_state_db(self, mac_address):
        db = self.waterflow_collection

        state = db.find_one({"MAC": mac_address}, {"_id": 0, "active": 1})
        
        return state
    
    def send_token_from_waterflow(self, token, mac_address):
        db_waterflow = self.waterflow_collection

        db_users = self.users_collection

        try:
            query = {
                "MAC": mac_address,
                "name": "New Waterflow",
                "stateHistory": [],
                "historyTemp": [],
                "currentTemp": 0,
                "autoCloseTemp": 0,
                "autoClose": False,
                "active": False
            }

            result = db_waterflow.insert_one(query)
            
            db_users.update_one(
                {"token": token},
                {"$push": {"waterflows": mac_address}}
            )

            return True
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def waterflow_in_database(self, mac_address):
        db = self.waterflow_collection

        waterflow = db.find_one({"MAC": mac_address})

        if waterflow:
            return True
        
        return False
    
    def get_waterflows_user(self, user_id):
        user = self.users_collection.find_one({"_id": ObjectId(user_id)}, {"_id": 0, "waterflows": 1})
        return user["waterflows"] if user else None
    
    def get_history_of_the_waterflow(self, mac_address):
        db = self.waterflow_collection
        result = db.find_one(
            {"MAC": mac_address},
            {"_id": 0, "stateHistory": 1}
        )
        if not result:
            return None
         
        raw_history_with_activate = result.get("stateHistory", [])
        results = []
        for doc in raw_history_with_activate:
            isoformated = doc.get("date", "").isoformat()
            results.append({
                "date": isoformated,
                "state": doc.get("state")
            })

        return results

    def get_information_waterflows(self, user_id):
        wf_ids = self.get_waterflows_user(user_id)
        if not wf_ids:
            return None

        try:
            object_ids = [wf for wf in wf_ids]
        except Exception:
            return None

        cursor = self.waterflow_collection.find(
            {"MAC": {"$in": object_ids}},
            {
                "_id": 1,
                "MAC": 1,
                "activate": 1,
                "stateHistory": 1,
                "historytemp": 1,
                "currentTemp": 1,
                "autoCloseTemp": 1,
                "autoClose": 1,
                "active": 1
            }
        )

        results = []
        for doc in cursor:
            doc["_id"] = str(doc["_id"])

            if "stateHistory" in doc:
                for entry in doc["stateHistory"]:
                    dt = entry.get("date")
                    entry["date"] = dt.isoformat() if hasattr(dt, "isoformat") else str(dt)

            if "historytemp" in doc:
                for entry in doc["historytemp"]:
                    dt = entry.get("date")
                    entry["date"] = dt.isoformat() if hasattr(dt, "isoformat") else str(dt)

            results.append(doc)

        return results


    def get_temperature_waterflow(self, mac_address):
        db = self.waterflow_collection
        waterflow = db.find_one(
            {"MAC": mac_address},
            {"_id": 0, "currentTemp": 1, "autoClose": 1, "autoCloseTemp": 1}
            )
        
        if not waterflow:
            return None

        return waterflow
    
    def get_history_temp(self, mac_address):
        db = self.waterflow_collection

        entry = db.find_one(
            {"MAC": mac_address},
            {"historytemp": 1, "_id": 0}
        )
        if not entry:
            return None

        raw_history_with_activate = entry.get("historytemp", [])

        results = []
        for doc in raw_history_with_activate:
            isoformated = doc.get("date", "").isoformat()
            results.append({
                "date": isoformated,
                "temp": doc.get("temp")
            })
        
        return results
    
    def send_temp(self, mac_address, temp):
        db = self.waterflow_collection
        local_zone = pytz.timezone('America/Chihuahua')
        local_date = datetime.now(local_zone)

        waterflow = db.find_one({"MAC": mac_address}, {"historyTemp": 1, "_id": 0})

        historyTemp = waterflow["historyTemp"]

        if not historyTemp:
            print("NOT HISTORY TEMP FOUND")
            return False
        
        if len(historyTemp) > 30:
            historyTemp = historyTemp[-29:]
            historyTemp.append({
                "temp": temp,
                "date": local_date
            })

        try:
            db.update_one(
        {"MAC": mac_address},
        {
                "$set": {"currentTemp": temp, "historyTemp": historyTemp}
                }
            )
            return True
        except:
            print("ERROR IN UPDATING THE TEMP")
            return False
        
    def modify_waterflow_settings(self, mac_address, autoCloseTemp, autoClose, name):
        query = {
            "autoCloseTemp": int(autoCloseTemp),
            "autoClose": autoClose,
            "name": name
        }

        db = self.waterflow_collection

        try:
            db.update_one(
                {"MAC": mac_address},
                {"$set": query}
                )
            return True
        except:
            return  False      

model_waterflow = Waterflow_model()