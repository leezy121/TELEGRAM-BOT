import telebot
from telebot import types

# Your bot token here
TOKEN = '7544072344:AAEq9jwGyXCysq662Gy_u8kS7quhA4DIWc4'
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user data
user_data = {}

# Function to create the main menu keyboard
def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Start', 'Tasks', 'Balance', 'Get Referral Code', 'Logout', 'Main Menu')
    return markup

# Function to handle the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id
    user_data[user_id] = {
        'logged_in': False,
        'balance': 300,  # Starting balance
        'referred': 0,   # Number of referrals
        'claimed_task': False,  # Track if task has been completed
        'task_answered': False  # Track if task has been attempted
    }
    bot.send_message(
        message.chat.id,
        "👋 Welcome to the Cats Airdrop! Please enter your Telegram username (must start with @):",
        reply_markup=types.ReplyKeyboardRemove()
    )
    bot.register_next_step_handler(message, handle_username)

# Function to handle the username input
def handle_username(message):
    user_id = message.from_user.id
    username = message.text
    if username.startswith('@'):
        user_data[user_id]['username'] = username
        bot.send_message(
            message.chat.id,
            "🐱 Great! Now please provide your TON wallet address:",
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, handle_wallet_address)
    else:
        bot.send_message(
            message.chat.id,
            "🚫 Invalid username. It must start with @. Please try again.",
            reply_markup=types.ReplyKeyboardRemove()
        )
        bot.register_next_step_handler(message, handle_username)

# Function to handle the wallet address input
def handle_wallet_address(message):
    user_id = message.from_user.id
    wallet_address = message.text
    # Add basic validation for the TON address format here if needed
    user_data[user_id]['wallet_address'] = wallet_address
    user_data[user_id]['logged_in'] = True
    bot.send_message(
        message.chat.id,
        "🎉 Congratulations! You have successfully qualified for the Cats Airdrop!\n\n"
        "Your current balance is: 300 Cats\n\n"
        "Exchange rate: 1000 Cats = $10\n\n"
        "You can withdraw once you reach 3000 Cats. Each referral earns you 100 Cats.\n\n"
        "Click 'Get Referral Code' to get your referral link.",
        reply_markup=create_main_menu_markup()
    )

# Function to handle the 'Tasks' button
@bot.message_handler(func=lambda message: message.text == 'Tasks')
def handle_tasks(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if user_data[user_id].get('claimed_task', False):
            bot.send_message(
                message.chat.id,
                "✅ You have already completed this task. Click 'Menu' for more options.",
                reply_markup=create_main_menu_markup()
            )
            return
        
        bot.send_message(
            message.chat.id,
            "📋 **TASKS SECTION**\n\n"
            "To complete this task and earn 500 Cats, watch the video below and listen to what the video is promoting.\n\n"
            "[Watch Video and Subscribe](https://www.tiktok.com/@leezymike1/video/7406511348592725254?is_from_webapp=1&sender_device=pc&web_id=7392496545273349637)\n\n"
            "After watching, type the name of the campaign that the owner of the video was advertising.\n\n"
            "Complete this task to get 500 Cats added to your balance.\n\n"
            "Click 'Menu' to return to the main menu.",
            reply_markup=types.ReplyKeyboardMarkup(
                resize_keyboard=True
            ).add('Menu')
        )
        bot.register_next_step_handler(message, handle_task_answer)
    else:
        bot.send_message(
            message.chat.id,
            "🚫 You are not logged in. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Function to handle the task answer
def handle_task_answer(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if user_data[user_id].get('claimed_task', False):
            bot.send_message(
                message.chat.id,
                "✅ You have already completed this task. Click 'Menu' for more options.",
                reply_markup=create_main_menu_markup()
            )
            return

        answer = message.text.lower().strip()
        if answer in ['clicksense', 'click sense']:
            user_data[user_id]['balance'] += 500
            user_data[user_id]['claimed_task'] = True
            bot.send_message(
                message.chat.id,
                "🎉 You are correct! Here is 500 Cats added to your balance.\n\n"
                "Your new balance is: {} Cats\n\n"
                "Click 'Menu' to return to the main menu.".format(user_data[user_id]['balance']),
                reply_markup=create_main_menu_markup()
            )
        else:
            bot.send_message(
                message.chat.id,
                "🚫 You are wrong and will not receive the task reward. Please only provide the correct campaign name.\n\n"
                "Click 'Menu' to return to the main menu.",
                reply_markup=create_main_menu_markup()
            )
    else:
        bot.send_message(
            message.chat.id,
            "🚫 You are not logged in. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Function to handle the 'Get Referral Code' button
@bot.message_handler(func=lambda message: message.text == 'Get Referral Code')
def handle_referral_code(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        referral_link = f"https://t.me/YourBot?start={user_id}"
        bot.send_message(
            message.chat.id,
            "🔗 Your referral link:\n\n" + referral_link + "\n\n"
            "Share this link with others to earn 100 Cats for each person who joins using your link.\n\n"
            "Click 'Menu' to return to the main menu.",
            reply_markup=create_main_menu_markup()
        )
    else:
        bot.send_message(
            message.chat.id,
            "🚫 You are not logged in. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Function to handle the 'Main Menu' button
@bot.message_handler(func=lambda message: message.text == 'Main Menu')
def handle_main_menu(message):
    user_id = message.from_user.id
    bot.send_message(
        message.chat.id,
        "👋 Welcome to the Cats Airdrop!\n\n"
        "Here’s how you can earn more Cats and what you can do:\n\n"
        "1. **Start** - Sign up or re-enter your details.\n"
        "2. **Tasks** - Complete tasks to earn Cats.\n"
        "3. **Balance** - Check your current balance.\n"
        "4. **Get Referral Code** - Get your unique referral link to earn Cats for each new user.\n"
        "5. **Logout** - Log out and sign up again.\n\n"
        "Click 'Menu' to return to the main menu.",
        reply_markup=create_main_menu_markup()
    )

# Function to handle the 'Logout' button
@bot.message_handler(func=lambda message: message.text == 'Logout')
def handle_logout(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data[user_id]['logged_in'] = False
        user_data[user_id]['claimed_task'] = False  # Reset task status on logout
        bot.send_message(
            message.chat.id,
            "You have been logged out. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Function to handle the 'Balance' button
@bot.message_handler(func=lambda message: message.text == 'Balance')
def handle_balance(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        bot.send_message(
            message.chat.id,
            "📊 Your current balance is: {} Cats\n\n".format(user_data[user_id]['balance']) +
            "Click 'Menu' to return to the main menu.",
            reply_markup=create_main_menu_markup()
        )
    else:
        bot.send_message(
            message.chat.id,
            "🚫 You are not logged in. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Function to handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if user_data[user_id].get('claimed_task', False):
            bot.send_message(
                message.chat.id,
                "🚫 You have already claimed your reward. Click 'Menu' to return to the main menu.",
                reply_markup=create_main_menu_markup()
            )
        else:
            bot.send_message(
                message.chat.id,
                "🚫 You have put a wrong command. Click 'Menu' to return to the main menu.",
                reply_markup=create_main_menu_markup()
            )
    else:
        bot.send_message(
            message.chat.id,
            "🚫 You are not logged in. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove()
        )

# Polling the bot
bot.polling()
