from typing import Any, Literal
from app.utils.db_utils import get_cursor, exec_commit 

class AuthenticationModel:
    def __init__(self) -> None:
        self.cur = None
    
    def openCursor(self) -> None:
        """Open database cursor if not already open"""
        if not self.cur:
            self.cur = get_cursor()
            
    def closeCursor(self) -> None:
        """Close database cursor if open"""
        if self.cur:
            self.cur.close()
            self.cur = None

    def commitQuery(self) -> None:
        """Commit current transaction"""
        if self.cur:
            self.cur = exec_commit()
            
    def insert_user(self, username, email, password) -> Literal['Sign up successfull.'] | Literal['User creation error.']:
        """Insert a new user into the database"""
        try:
            self.openCursor()
            if not self.cur:
                raise Exception("Failed to open database cursor")
                
            query = 'INSERT INTO users(username, gmail, password) VALUES (%s, %s, %s)'
            values: tuple = (username, email, password)
            
            self.cur.execute(query, values)
            self.commitQuery()
            self.closeCursor()
            return "Sign up successfull."
            
        except Exception as error:
            print(f"Error inserting user: {error}")
            self.closeCursor()
            return "User creation error."
        
    def get_user(self, username, password) -> Any | None:
        """Get user by username and password"""
        try:
            self.openCursor()
            if not self.cur:
                raise Exception("Failed to open database cursor")
                
            query = "SELECT * FROM users WHERE username = %s and password = %s"
            values: tuple = (username, password)
            
            self.cur.execute(query, values)
            response = self.cur.fetchone()
            
            self.closeCursor()
            return response if response else None
            
        except Exception as error:
            print(f"Error getting user: {error}")
            self.closeCursor()
            return None