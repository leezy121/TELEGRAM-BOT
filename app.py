from flask import Flask, request
import telebot
from telebot import types
import threading

app = Flask(__name__)

# Your bot token here
TOKEN = '7544072344:AAEq9jwGyXCysq662Gy_u8kS7quhA4DIWc4'
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user data
user_data = {}

# Function to create the main menu keyboard
def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Tasks', 'Balance', 'Get Referral Code', 'Withdrawal', 'Logout', 'Main Menu')
    return markup

# Function to create the tasks menu keyboard
def create_tasks_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Task 1', 'Task 2', 'Main Menu')
    return markup

# Function to create the start keyboard (for new users or logged out users)
def create_start_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Start')
    return markup

# Function to validate TON wallet address (at least 30 characters)
def is_valid_ton_wallet_address(address):
    return len(address) >= 30

@app.route('/webhook', methods=['POST'])
def webhook():
    json_str = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return 'OK', 200

def set_webhook():
    url = 'https://telegram-bot-2-k7tg.onrender.com/Webhook'  # Replace with your actual Render service URL
    response = bot.set_webhook(url=url)
    print('Webhook set:', response)

def run_flask():
    app.run(host='0.0.0.0', port=10000)

if __name__ == '__main__':
    # Start the webhook setup in a separate thread
    threading.Thread(target=set_webhook).start()
    # Run the Flask app
    run_flask()
