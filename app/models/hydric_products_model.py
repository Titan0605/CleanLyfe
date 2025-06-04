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
        
    
    # def validate_email(self, email: str) -> bool:
    #     """Validate email format"""
    #     pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'
    #     return bool(re.match(pattern, email))
    
    # def validate_username(self, username: str) -> bool:
    #     """Validate username format and uniqueness"""
    #     if len(username) < 3:
    #         return False
    #     existing_user = self.users_collection.find_one({"user_name": username})
    #     return existing_user is None
    
    # def create_user(self, user_info: Dict[str, str]) -> Dict[str, str]:
    #     """Create a new user with validation"""
    #     # Validate email format
    #     if not self.validate_email(user_info["email"]):
    #         return {"status": "error", "message": "Invalid email format"}
            
    #     # Validate username
    #     if not self.validate_username(user_info["username"]):
    #         return {"status": "error", "message": "Username already exists or is invalid"}
            
    #     # Create new user document
    #     new_user = {
    #         "first_name": user_info["firstname"],
    #         "last_name": user_info["lastname"],
    #         "user_name": user_info["username"],
    #         "email": user_info["email"],
    #         "password": generate_password_hash(user_info["password"]),
    #         "member_type": "user",
    #         "water_flows": [],
    #         "active": True,
    #         "created_at": datetime.now(timezone.utc),
    #         "updated_at": []
    #     }
        
    #     try:
    #         self.users_collection.insert_one(new_user)
    #         return {"status": "success", "message": "Sign up successful"}
    #     except Exception as error:
    #         return {"status": "error", "message": str(error)}
        
    # def get_user(self, user_credentials: Dict[str, str]) -> Optional[Dict[str, Any]]:
    #     """Get user and verify credentials"""
    #     try:
    #         user = self.users_collection.find_one({"user_name": user_credentials["username"]})
            
    #         if user and check_password_hash(user["password"], user_credentials["password"]):
    #             # Remove password from returned user object
    #             user.pop("password", None)
    #             return user
    #         return None
            
    #     except Exception as error:
    #         print(f"Error getting user: {error}")
    #         return None