import sqlite3
import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect("requests.db")
        self.conn.execute("CREATE TABLE IF NOT EXISTS requests (id INTEGER PRIMARY KEY AUTOINCREMENT, text TEXT, date_time TEXT)")
        self.conn.execute("CREATE TABLE IF NOT EXISTS remaining (id INTEGER PRIMARY KEY AUTOINCREMENT, value INTEGER)")
        self.conn.commit()
        self.conn.execute("INSERT INTO remaining (value) VALUES (10)")
        self.conn.commit()



    def add_request(self, text):
        cursor = self.conn.execute("SELECT * FROM remaining")
        remaining = cursor.fetchone()[1]
        if remaining > 0:
            current_datetime = str(datetime.datetime.now())
            self.conn.execute("INSERT INTO requests (text, date_time) VALUES (?,?)", (text, current_datetime))
            self.conn.commit()
            self.conn.execute("UPDATE remaining SET value=value-1 WHERE id=1")
            self.conn.commit()
            return True
        else:
            return False

    def get_total_requests(self):
        cursor = self.conn.execute("SELECT COUNT(*) FROM requests")
        return cursor.fetchone()[0]

    def get_remaining_left(self):
        cursor = self.conn.execute("SELECT * FROM remaining")
        return cursor.fetchone()[1]

    def get_last_request_date(self):
        cursor = self.conn.execute("SELECT date_time FROM requests ORDER BY id DESC LIMIT 1")
        last_request_date = cursor.fetchone()
        if last_request_date: return last_request_date[0]
        return str(datetime.datetime.now())
    
    def reset_limit(self, new_limit=0):
        self.conn.execute("UPDATE remaining SET value=? WHERE id=1", (new_limit,))
        self.conn.commit()
