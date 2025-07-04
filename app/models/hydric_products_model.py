from app.utils.db_utils import get_client, get_collection
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from flask import session
from typing import Optional, Dict, Any
class Hydric_products_model:
    def __init__(self) -> None:
        self._client: Optional[MongoClient] = None
        self._users_collection: Optional[Collection] = None
        
    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = get_client()
        return self._client
    
    @property
    def footprints_collection(self) -> Collection:
        if self._users_collection is None:
            self._users_collection = get_collection("footprintCalculations")
        return self._users_collection
    
    def save_hydric_footprint(self, data: dict) -> Dict[str, str]: 
        new_hydric_footprint = {
            "userId": ObjectId(session['id']),
            "calculationType": "Hydric",
            "createdAt": datetime.now(timezone.utc),
            "active": True,
            "hydricFootprint": {
                "totalHydricFootprint": data['total_hydric_footprint'],
                "normalWaterConsumption": {
                    "showerConsumption": data['shower_consumption'],
                    "toiletConsumption": data['toilet_consumption'],
                    "dishesConsumption": data['dishes_consumption'],
                    "washingMachineConsumption": data['washing_machine_consumption'],
                    "gardenConsumption": data['garden_consumption'],
                    "houseCleaning": data['house_cleaning_consumption'],
                    "totalWaterConsumption": data['normal_water_consumption']
                },
                "productsWaterConsumption": {
                    "totalWaterConsumption": data['products_water_consumption'],
                    "productsConsumptions": data['products']
                }
            }
        }
        
        try:
            self.footprints_collection.insert_one(new_hydric_footprint)
            return {"status": "success", "message": "Hydric footprint successfully saved"}
        except Exception as error:
            return {"status": "error", "message": str(error)}