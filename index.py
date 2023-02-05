import telebot
import os
import requests
TOKEN = os.getenv("TELEBOT_TOKEN", "No token provided")
URL = os.getenv("URL", "http://localhost:3000/download-chart")
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=["test"])
def send_welcome(message):
    bot.reply_to(message, "Working.....")

@bot.message_handler(commands=['download'])
def handle_download_card(message):
    try:
        # Get the input text from the user's message
        date = message.text.split("\n")[1]
        data = message.text.split("\n")[2].split(",")
        # Make a POST request to the API endpoint
        response = requests.post(URL, json={"date": date, "data" : data})

        print(response.status_code)
        # Check that the request was successful
        if response.status_code == 200:
            # Send the PNG image to the user as a photo
            bot.send_photo(chat_id=message.chat.id, photo=response.content)
        else:
            bot.send_message(chat_id=message.chat.id, text="Failed to get image: ")
    except:
           bot.send_message(chat_id=message.chat.id, text="Something wrong with logic.")

@bot.message_handler(func=lambda message: True)
def show_options(message):
    bot.reply_to(message, "Welcome! I am your bot, will help you to get chart.\n")

bot.polling()
