import os
import requests
import telebot
import json

from flask import Flask, request

app = Flask(__name__)


URL="https://poster-api-zjej.onrender.com/download-chart/"
BOT_TOKEN="6085972993:AAFc8Vibup_2vZP1lueN5ABqywwrkEEY8DQ"
TEXT_URL=f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
PHOTO_URL=f"https://api.telegram.org/bot{BOT_TOKEN}/sendPhoto"
ACTION_URL=f"https://api.telegram.org/bot{BOT_TOKEN}/sendChatAction"


def send_message(message):
    pass

@app.route('/', methods=['POST'])
def handle_command():
    message = "/download\n12-12-2022\n1,2,3"
    date = message.split("\n")[1]
    data = message.split("\n")[2].split(",")
    data = {"data": data, "date": date}
    headers = {'Content-Type': 'application/json'}
    response = requests.post(URL, data=json.dumps(data), headers=headers)
    url = "https://api.telegram.org/bot{token}/sendPhoto".format(token=BOT_TOKEN)
    files = {"photo": ("image.jpg", response.content, "image/jpeg")}
    data = {"chat_id": 1316144383}

    # Make the API request
    response = requests.post(url, files=files, data=data)
    print(response.content)
    # Check the response status code
    if response.status_code != 200:
        return "Failed to send photo to Telegram", 500
    else:
        return "Photo sent successfully", 200
    

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
