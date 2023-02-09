import os
import requests
import telebot
from flask import Flask, request

from command import StartCommand, HelpCommand, DefaultCommand, DownloadCommand, TotalCommand, LimitCommand

commands = {
    "/start": StartCommand,
    "/help": HelpCommand,
    "/download" : DownloadCommand,
    "/total" : TotalCommand,
    "/limit" : LimitCommand
}

app = Flask(__name__)


BOT_TOKEN = os.getenv('BOT_TOKEN')
TEXT_URL = os.getenv('TEXT_URL')
PHOTO_URL = os.getenv('PHOTO_URL')
ACTION_URL = os.getenv('ACTION_URL')


def send_message(message):
    chat_id = message.get("chat_id", "default_value")
    try:
        text_message = message.get("type")
        response = message.get("response", "response")
        bot = telebot.TeleBot(BOT_TOKEN)
        print(BOT_TOKEN)
        if text_message == "text":
            print("response type is text")
            requests.post(ACTION_URL, json={"chat_id": chat_id, "action": "typing"})
            response = requests.post(TEXT_URL, json={"chat_id": chat_id, "text": response})
            if response.status_code != 200:
                print(response.content)
            return None
        print("response type is other than text")
        requests.post(ACTION_URL, json={"chat_id": chat_id, "action": "uploading_photo"})
        files = {"photo": ("image.jpg", response, "image/jpeg")}
        data = {"chat_id": chat_id}
    
        # Make the API request
        response = requests.post(PHOTO_URL, files=files, data=data)
        print(response.content)
    except Exception as e:
        print(e)
        requests.post(TEXT_URL, json={"chat_id": chat_id, "text": response})

@app.route('/', methods=['POST'])
def handle_command():
    try:
        print("request recieved....")
        update = request.get_json()
        chat_id = update['message']['chat']['id']
        message = update['message']['text']

        command = commands.get(message.split("\n")[0], DefaultCommand)
        
        print("command loaded")
        
        response = command(message).get_response(message)
        
        print("command executed")
        
        response["chat_id"] = chat_id
        
        send_message(response)
        
        print("response sent")
        return "OK" , 200
    except Exception as e:
        print(e)
        return "Internal server error in main" , 502
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
