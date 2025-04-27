from app.utils.db_utils import get_cursor, get_commit 

class Electric_devices_model:
    def __init__(self):
        self.cur = None
    # Method to get the cursor
    def openCursor(self):
        if not self.cur:
            self.cur = get_cursor()
    def commitQuery(self):
        if self.cur:
            self.cur = get_commit()
    # Method to close the cursor
    def closeCursor(self):
        if self.cur:
            self.cur.close()
            self.cur = None
    
    def getAllDevices(self):
        try:
            self.openCursor()
            query = "SELECT * FROM devices"
            self.cur.execute(query)
            response = self.cur.fetchall()
            if not response:
                self.closeCursor()
                return None
            else:
                self.closeCursor()
                return response
        except KeyError as e:
            print("Error: ", e)
            return None

    # Gets the device by its id
    def getDeviceById(self, deviceId):
        try:
            self.openCursor()
            query = "SELECT * FROM devices WHERE id = %s"
            values = (deviceId,)
            self.cur.execute(query, values)
            response = self.cur.fetchone()
            if not response:
                self.closeCursor()
                return None
            else:
                self.closeCursor()
                return response
        except KeyError as e:
            print("Error: ", e)
            return None
    
    # Gets the device by its name
    def getDeviceByName(self, deviceName):
        try:
            self.openCursor()
            query = "SELECT * FROM devices WHERE name = %s"
            values = (deviceName,)
            self.cur.execute(query, values)
            response = self.cur.fetchone()
            if not response:
                self.closeCursor()
                return None
            else:
                self.closeCursor()
                return response
        except KeyError as e:
            print("Error: ", e)
            return None

    # Gets all the devices by its location
    def getDeviceByLocation(self, deviceLocation):
        try:
            self.openCursor()
            query = "SELECT * FROM devices WHERE location = %s"
            values = (deviceLocation,)
            self.cur.execute(query, values)
            response = self.cur.fetchall()
            if not response:
                self.closeCursor()
                return None
            else:
                self.closeCursor()
                return response
        except KeyError as e:
            print("Error: ", e)
            return None
        
    # Gets the device name by its id
    def getDeviceNameById(self, deviceId):
        try:
            self.openCursor()
            query = "SELECT name FROM devices WHERE id = %s"
            values = (deviceId,)
            self.cur.execute(query, values)
            response = self.cur.fetchone()
            if not response:
                self.closeCursor()
                return None
            else:
                self.closeCursor()
                return response
        except KeyError as e:
            print("Error: ", e)
            return None