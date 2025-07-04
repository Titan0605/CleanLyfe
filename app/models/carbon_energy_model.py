from app.utils.db_utils import get_client, get_collection
from pymongo import MongoClient
from pymongo.collection import Collection
from bson.objectid import ObjectId
from typing import Optional, Dict, Any

class ElectricDevicesModel:
    def __init__(self) -> None:
        self._client: Optional[MongoClient] = None
        self._devices_catalog_collection: Optional[Collection] = None
        self._devices_collection: Optional[Collection] = None
        
    @property
    def client(self) -> MongoClient:
        if self._client is None:
            self._client = get_client()
        return self._client
    
    @property
    def devices_catalog_collection(self) -> Collection:
        if self._devices_catalog_collection is None:
            self._devices_catalog_collection = get_collection("deviceCatalog")
        return self._devices_catalog_collection
    
    @property
    def devices_collection(self) -> Collection:
        if self._devices_collection is None:
            self._devices_collection = get_collection("energyDevices")
        return self._devices_collection
    
    def get_all_devices(self):
        devices = []
        
        devices_catalog = self.devices_catalog_collection.find().sort("deviceZone")
        for device in devices_catalog:
            modified_device = {
                "id": str(device["_id"]),
                "deviceName": device["deviceName"],
                "deviceZone": device["deviceZone"]
            }
            devices.append(modified_device)
        print(devices)
        
        return tuple(devices)
    
    def get_devices_by_ids(self, ids_list):
        object_ids = [ObjectId(id_str) for id_str in ids_list]
        query = {"_id": {"$in": object_ids}}
        devices = []
        
        devices_catalog = self.devices_catalog_collection.find(query).sort("deviceName")
        for device in devices_catalog:
            modified_device = {
                "id": str(device["_id"]),
                "deviceName": device["deviceName"],
                "deviceZone": device["deviceZone"]
            }
            devices.append(modified_device)
        print(devices)
        
        return tuple(devices)
    
    def calculate_energy_footprint(self, data):
        user_devices_ids = self._insert_devices(data["devices"])
        
        energy_calculus = {
            "totalEnergyConsumption": data["totalConsumption"],
            "totalEmission": data["totalEmission"],
            "devices": user_devices_ids
        }
        
        return energy_calculus
    
    def _insert_devices(self, devices):
        documents = []
        
        for device in devices:
            device_insert = {
                "deviceType": ObjectId(device["id"]),
                "deviceActivePower": device["deviceActivePower"],
                "activeUsedHours": device["activeUsedHours"],
                "deviceStandbyPower": device["deviceStandbyPower"],
                "standbyUsedHours": device["standbyUsedHours"],
                "deviceEfficiency": device["deviceEfficiency"],
                "activeConsume": device["activeConsume"],
                "standbyConsume": device["standbyConsume"],
                "adjustedActiveConsume": device["adjustedActiveConsume"],
                "adjustedStandbyConsume": device["adjustedStandbyConsume"],
                "totalDailyConsumption": device["totalDailyConsumption"],
                "totalWeeklyConsumption": device["totalWeeklyConsumption"],
                "weeklyCarbonEmission": device["weeklyCarbonEmission"]
            }
            documents.append(device_insert)
            
        result = self.devices_collection.insert_many(documents)
        
        generated_ids = result.inserted_ids
        
        return tuple(generated_ids)
            

# class Electric_devices_model:
#     def __init__(self) -> None:
#         self.cur = None
        
#     def openCursor(self) -> None:
#         """Open database cursor if not already open"""
#         if not self.cur:
#             self.cur = get_cursor()
            
#     def commitQuery(self) -> None:
#         """Commit current transaction"""
#         if self.cur:
#             self.cur = exec_commit()
            
#     def closeCursor(self) -> None:
#         """Close database cursor if open"""
#         if self.cur:
#             self.cur.close()
#             self.cur = None
    
#     def getAllDevices(self) -> Any | None:
#         """Get all devices from database"""
#         try:
#             self.openCursor()
#             if not self.cur:
#                 raise Exception("Failed to open database cursor")
                
#             query = "SELECT * FROM devices"
#             self.cur.execute(query)
#             response = self.cur.fetchall()
            
#             self.closeCursor()
#             return response if response else None
            
#         except Exception as error:
#             print(f"Error getting all devices: {error}")
#             self.closeCursor()
#             return None

#     def getDeviceById(self, deviceId) -> Any | None:
#         """Get device by its ID"""
#         try:
#             self.openCursor()
#             if not self.cur:
#                 raise Exception("Failed to open database cursor")
                
#             query = "SELECT * FROM devices WHERE id = %s"
#             values: tuple = (deviceId,)
            
#             self.cur.execute(query, values)
#             response = self.cur.fetchone()
            
#             self.closeCursor()
#             return response if response else None
            
#         except Exception as error:
#             print(f"Error getting device by ID: {error}")
#             self.closeCursor()
#             return None
    
#     def getDeviceByName(self, deviceName) -> Any | None:
#         """Get device by its name"""
#         try:
#             self.openCursor()
#             if not self.cur:
#                 raise Exception("Failed to open database cursor")
                
#             query = "SELECT * FROM devices WHERE name = %s"
#             values: tuple = (deviceName,)
            
#             self.cur.execute(query, values)
#             response = self.cur.fetchone()
            
#             self.closeCursor()
#             return response if response else None
            
#         except Exception as error:
#             print(f"Error getting device by name: {error}")
#             self.closeCursor()
#             return None

#     def getDeviceByLocation(self, deviceLocation) -> Any | None:
#         """Get all devices by location"""
#         try:
#             self.openCursor()
#             if not self.cur:
#                 raise Exception("Failed to open database cursor")
                
#             query = "SELECT * FROM devices WHERE location = %s"
#             values: tuple = (deviceLocation,)
            
#             self.cur.execute(query, values)
#             response = self.cur.fetchall()
            
#             self.closeCursor()
#             return response if response else None
            
#         except Exception as error:
#             print(f"Error getting devices by location: {error}")
#             self.closeCursor()
#             return None
        
#     def getDeviceIdNameById(self, deviceId) -> Any | None:
#         """Get device ID and name by its ID"""
#         try:
#             self.openCursor()
#             if not self.cur:
#                 raise Exception("Failed to open database cursor")
                
#             query = "SELECT id, name FROM devices WHERE id = %s"
#             values: tuple = (deviceId,)
            
#             self.cur.execute(query, values)
#             response = self.cur.fetchone()
            
#             self.closeCursor()
#             return response if response else None
            
#         except Exception as error:
#             print(f"Error getting device ID and name: {error}")
#             self.closeCursor()
#             return None