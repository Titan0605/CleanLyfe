from typing import Any
from app.utils.db_utils import get_cursor, get_commit 

class Electric_devices_model:
    def __init__(self) -> None:
        self.cur = None
        
    def openCursor(self) -> None:
        """Open database cursor if not already open"""
        if not self.cur:
            self.cur = get_cursor()
            
    def commitQuery(self) -> None:
        """Commit current transaction"""
        if self.cur:
            self.cur = get_commit()
            
    def closeCursor(self) -> None:
        """Close database cursor if open"""
        if self.cur:
            self.cur.close()
            self.cur = None
    
    def getAllDevices(self) -> Any | None:
        """Get all devices from database"""
        try:
            self.openCursor()
            if not self.cur:
                raise Exception("Failed to open database cursor")
                
            query = "SELECT * FROM devices"
            self.cur.execute(query)
            response = self.cur.fetchall()
            
            self.closeCursor()
            return response if response else None
            
        except Exception as error:
            print(f"Error getting all devices: {error}")
            self.closeCursor()
            return None

    def getDeviceById(self, deviceId) -> Any | None:
        """Get device by its ID"""
        try:
            self.openCursor()
            if not self.cur:
                raise Exception("Failed to open database cursor")
                
            query = "SELECT * FROM devices WHERE id = %s"
            values: tuple = (deviceId,)
            
            self.cur.execute(query, values)
            response = self.cur.fetchone()
            
            self.closeCursor()
            return response if response else None
            
        except Exception as error:
            print(f"Error getting device by ID: {error}")
            self.closeCursor()
            return None
    
    def getDeviceByName(self, deviceName) -> Any | None:
        """Get device by its name"""
        try:
            self.openCursor()
            if not self.cur:
                raise Exception("Failed to open database cursor")
                
            query = "SELECT * FROM devices WHERE name = %s"
            values: tuple = (deviceName,)
            
            self.cur.execute(query, values)
            response = self.cur.fetchone()
            
            self.closeCursor()
            return response if response else None
            
        except Exception as error:
            print(f"Error getting device by name: {error}")
            self.closeCursor()
            return None

    def getDeviceByLocation(self, deviceLocation) -> Any | None:
        """Get all devices by location"""
        try:
            self.openCursor()
            if not self.cur:
                raise Exception("Failed to open database cursor")
                
            query = "SELECT * FROM devices WHERE location = %s"
            values: tuple = (deviceLocation,)
            
            self.cur.execute(query, values)
            response = self.cur.fetchall()
            
            self.closeCursor()
            return response if response else None
            
        except Exception as error:
            print(f"Error getting devices by location: {error}")
            self.closeCursor()
            return None
        
    def getDeviceIdNameById(self, deviceId) -> Any | None:
        """Get device ID and name by its ID"""
        try:
            self.openCursor()
            if not self.cur:
                raise Exception("Failed to open database cursor")
                
            query = "SELECT id, name FROM devices WHERE id = %s"
            values: tuple = (deviceId,)
            
            self.cur.execute(query, values)
            response = self.cur.fetchone()
            
            self.closeCursor()
            return response if response else None
            
        except Exception as error:
            print(f"Error getting device ID and name: {error}")
            self.closeCursor()
            return None