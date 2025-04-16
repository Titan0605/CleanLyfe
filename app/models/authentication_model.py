from app.utils.db_utils import get_cursor, get_commit 

class AuthenticationModel:
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
    def insert_user(self, username, email, password):
        try:
            self.openCursor()
            query = 'INSERT INTO users(username, gmail, password) VALUES (%s, %s, %s)'
            values = (username, email, password,)
            self.cur.execute(query, values)
            self.commitQuery()
            self.closeCursor()
            return "Sign up successfull."
        except KeyError as error:
            print(error)
            return "User creation error."
    def get_user(self, username, password):
        try:
            self.openCursor()
            query = "SELECT * FROM users WHERE username = %s and password = %s"
            values = (username, password,)
            self.cur.execute(query, values)
            response = self.cur.fetchall()
            self.closeCursor()
            return "Login successfull.", response
        except KeyError as e:
            response = None
            return "Login error, credentials incorrects.", response