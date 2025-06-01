from app.utils.db_utils import get_client, get_collection
from datetime import datetime, timezone
from pymongo import MongoClient
from pymongo.collection import Collection
from typing import Optional
class AuthenticationModel:
    def __init__(self) -> None:
        self._client: Optional[MongoClient] = None
        self._users_collection: Optional[Collection] = None
        
    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = get_client()
        return self._client
    
    @property
    def users_collection(self) -> Collection:
        if self._users_collection is None:
            self._users_collection = get_collection("users")
        return self._users_collection
    
    def create_user(self, user_info: dict):
        new_user = {
            "firstName": user_info["first_name"],
            "lastName": user_info["last_name"],
            "userName": user_info["user_name"],
            "email": user_info["email"],
            "password": user_info["password"],
            "memberType": "user",
            "waterFlows": [],
            "active": True,
            "createdAt": datetime.now(timezone.utc),
            "updatedAt": []
        }
        
        try:
            self.users_collection.insert_one(new_user)
            return "Sign up successfull."
        except Exception as error:
            print(f"Error inserting user: {error}")
            return "User creation error."
        
    def get_user(self, user_credentials: dict):
        query = {
            "userName": user_credentials["username"]
        }
        
        try:
            user = self.users_collection.find_one(query)
            return user if user else None
        except Exception as error:
            print(f"Error getting user: {error}")
            return None