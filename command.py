import requests
import json
import os
from database import Database
import datetime


URL = os.getenv("URL", "http://localhost:3000/download-chart")
class Command:
    def __init__(self, message):
        self.message = message

    def get_response(self, message):
        pass

class StartCommand(Command):
    def get_response(self, message):
        return {"response": "Hello! How can I help you?", "type" : "text"} 

class HelpCommand(Command):
    def get_response(self, message):
        return {"response": '''format for download chart is below\n\n/download\n31-12-2022\n1,2,3''', "type" : "text"} 

class DefaultCommand(Command):
    def get_response(self, message):
        # print(URL)
        return {"response": "You said: " + self.message, "type" : "text"} 

class TotalCommand(Command):
    def get_response(self, message):
        db = Database()
        return {"response": "Total request: " + str(db.get_total_requests()), "type" : "text"} 

class LimitCommand(Command):
    def get_response(self, message):
        db = Database()
        return {"response": "Limit left: " + str(db.get_remaining_left()), "type" : "text"} 

class DownloadCommand(Command):
    def get_response(self, message):
        try:
            date = message.split("\n")[1]
            data = message.split("\n")[2].split(",")
            data = {"data": data, "date": date}
            headers = {'Content-Type': 'application/json'}
            try:
                db = Database()
                limit = db.get_remaining_left()
                date = db.get_last_request_date()
                last_request_datetime_str = db.get_last_request_date()
                last_request_datetime = datetime.datetime.strptime(last_request_datetime_str, "%Y-%m-%d %H:%M:%S.%f")
                current_datetime = datetime.datetime.now()
                time_diff = current_datetime - last_request_datetime
                if (limit <= 0 and time_diff.days <= 0) : 
                    return {"response": "Your daily limit is over", "type" : "text"}
                
                if (limit <= 0 and time_diff.days >= 1) : 
                    db.reset_limit()
                
                response = requests.post(URL, data=json.dumps(data), headers=headers)
                if response.status_code == 200:
                    db.add_request(str(date) + " : " + str(data))
                    return {"response": response.content, "type" : "photo"} 
                return {"response": response.content, "type" : "text"} 
            except Exception as e: 
                print("Something failed while calling poster api")
                print(e)       
                return {"response": "Something failed while calling poster api", "type" : "text"} 
        except Exception as e:
            print("Something failed while splitting the data")
            print(e)
            return {"response": "Something failed while splitting the data", "type" : "text"} 
