import telebot
from telebot import types

# Your bot token here
TOKEN = '7012072031:AAFnXWppm1zm8BRCr1SK6VR9TuBd_HxIwaE'
bot = telebot.TeleBot(TOKEN)

# Dictionary to store user data
user_data = {}


# Function to create the main menu keyboard
def create_main_menu_markup():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('Tasks', 'Balance', 'Get Referral Code', 'Withdrawal', 'Logout',
               'Main Menu')
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


# Function to handle the /start command
@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.from_user.id

    if user_id in user_data and user_data[user_id].get('logged_in', False):
        bot.send_message(
            message.chat.id, "🎉 You are already logged in! Welcome back! 🎉\n\n"
            "Click 'Main Menu' to explore more about the Cats Airdrop.",
            reply_markup=create_main_menu_markup())
        return

    user_data[user_id] = {'logged_in': False}
    bot.send_message(
        message.chat.id, "👋 Welcome to the **Cats Airdrop**! 🐾\n\n"
        "To get started, please enter your **Telegram username** (must start with @):",
        reply_markup=create_start_markup())
    bot.register_next_step_handler(message, handle_username)


# Function to handle the username input
def handle_username(message):
    user_id = message.from_user.id
    username = message.text

    if username.startswith('@'):
        bot.send_message(
            message.chat.id,
            "💼 Great! Now please provide your **TON wallet address** to complete the registration.\n\n"
            "Make sure it has at least 30 characters to receive the airdrop payment.",
            reply_markup=types.ReplyKeyboardRemove())
        user_data[user_id]['username'] = username
        bot.register_next_step_handler(message, handle_wallet_address)
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **Invalid username**. It must start with @. Please enter a valid username:",
            reply_markup=create_start_markup())
        bot.register_next_step_handler(message, handle_username)


# Function to handle the wallet address input
def handle_wallet_address(message):
    user_id = message.from_user.id
    wallet_address = message.text

    if is_valid_ton_wallet_address(wallet_address):
        user_data[user_id]['wallet_address'] = wallet_address
        user_data[user_id]['logged_in'] = True
        user_data[user_id]['balance'] = 300  # Starting balance
        user_data[user_id]['referred'] = 0  # Number of referrals
        user_data[user_id]['claimed_tasks'] = set()  # Track claimed tasks
        bot.send_message(
            message.chat.id, "🎉 **Congratulations!** 🎉\n\n"
            "You have successfully registered and received **300 Cats**! 🐱🎉\n\n"
            "Welcome to the **Cats Airdrop**. Here’s what you need to know:\n\n"
            "🔹 **Current Balance**: 300 Cats\n"
            "🔹 **Tasks**: Complete tasks to earn more Cats. Click 'Tasks' to get details.\n"
            "🔹 **Get Referral Code**: Share your link to earn Cats for each new user.\n"
            "🔹 **Balance**: Check how many Cats you have.\n"
            "🔹 **Withdrawal**: Request a withdrawal if you have enough Cats.\n"
            "🔹 **Logout**: Log out if you wish to sign up again.\n\n"
            "🎁 **Current Task**: Watch the video and identify the campaign name to earn **500 Cats**. Click 'Tasks' to start.",
            reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **Invalid TON wallet address**. Please make sure it has at least 30 characters.\n\n"
            "Enter a valid TON wallet address to continue and receive the airdrop payment:",
            reply_markup=types.ReplyKeyboardRemove())
        bot.register_next_step_handler(message, handle_wallet_address)


# Function to handle the 'Tasks' button
@bot.message_handler(func=lambda message: message.text == 'Tasks')
def handle_tasks(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        bot.send_message(
            message.chat.id, "📋 **TASKS SECTION**\n\n"
            "Choose a task to perform:\n\n"
            "1. **Task 1**: Watch the video and identify the campaign name to earn **500 Cats**.\n"
            "2. **Task 2**: Join the Telegram group to earn more tasks. Send 'ok' here after joining to collect **300 Cats**.\n",
            reply_markup=create_tasks_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle 'Task 1'
@bot.message_handler(func=lambda message: message.text == 'Task 1')
def handle_task_1(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if 'Task 1' in user_data[user_id]['claimed_tasks']:
            bot.send_message(
                message.chat.id,
                "✅ **You have already completed Task 1**. Click 'Main Menu' for more options.",
                reply_markup=create_main_menu_markup())
        else:
            bot.send_message(
                message.chat.id, "📋 **Task 1**\n\n"
                "To earn **500 Cats**, follow these steps:\n\n"
                "1. Watch the video below and listen to what the video is promoting.\n\n"
                "[Watch Video and Subscribe](https://www.tiktok.com/@leezymike1/video/7406511348592725254?is_from_webapp=1&sender_device=pc&web_id=7392496545273349637)\n\n"
                "2. After watching, type the name of the campaign that the owner of the video was advertising.\n\n"
                "💡 **Tip**: Be attentive to the video details to correctly identify the campaign.\n\n"
                "Complete this task to earn **500 Cats** added to your balance.\n\n"
                "Click 'Menu' to return to the main menu.",
                reply_markup=types.ReplyKeyboardMarkup(
                    resize_keyboard=True).add('Menu'))
            bot.register_next_step_handler(message, handle_task_1_answer)
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle the answer for 'Task 1'
def handle_task_1_answer(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if 'Task 1' in user_data[user_id]['claimed_tasks']:
            bot.send_message(
                message.chat.id,
                "✅ **You have already completed Task 1**. Click 'Main Menu' for more options.",
                reply_markup=create_main_menu_markup())
            return

        answer = message.text.lower().strip()
        if answer in ['clicksense', 'click sense']:
            user_data[user_id]['balance'] += 500
            user_data[user_id]['claimed_tasks'].add('Task 1')
            bot.send_message(message.chat.id,
                             "🎉 **Correct!** 🎉\n\n"
                             "You have earned **500 Cats**! 🐱💵\n\n"
                             "Your new balance is: **{} Cats**\n\n".format(
                                 user_data[user_id]['balance']) +
                             "Click 'Menu' to return to the main menu.",
                             reply_markup=create_main_menu_markup())
        else:
            bot.send_message(
                message.chat.id,
                "🚫 **Incorrect answer**. Please provide the correct campaign name to earn the reward.\n\n"
                "Click 'Menu' to return to the main menu.",
                reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle 'Task 2'
@bot.message_handler(func=lambda message: message.text == 'Task 2')
def handle_task_2(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if 'Task 2' in user_data[user_id]['claimed_tasks']:
            bot.send_message(
                message.chat.id,
                "✅ **You have already completed Task 2**. Click 'Main Menu' for more options.",
                reply_markup=create_main_menu_markup())
        else:
            bot.send_message(
                message.chat.id, "📋 **Task 2**\n\n"
                "To earn **300 Cats**, join the following Telegram group:\n\n"
                "[Join Telegram Group](https://t.me/+PSazTgIhmV0yZGE0)\n\n"
                "After joining, type 'ok' here to confirm your participation.\n\n"
                "Click 'Menu' to return to the main menu.",
                reply_markup=types.ReplyKeyboardMarkup(
                    resize_keyboard=True).add('Menu'))
            bot.register_next_step_handler(message, handle_task_2_confirmation)
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle confirmation for 'Task 2'
def handle_task_2_confirmation(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if 'Task 2' in user_data[user_id]['claimed_tasks']:
            bot.send_message(
                message.chat.id,
                "✅ **You have already completed Task 2**. Click 'Main Menu' for more options.",
                reply_markup=create_main_menu_markup())
            return

        if message.text.lower() == 'ok':
            user_data[user_id]['balance'] += 300
            user_data[user_id]['claimed_tasks'].add('Task 2')
            bot.send_message(message.chat.id,
                             "🎉 **Confirmation received!** 🎉\n\n"
                             "You have earned **300 Cats**! 🐱💵\n\n"
                             "Your new balance is: **{} Cats**\n\n".format(
                                 user_data[user_id]['balance']) +
                             "Click 'Menu' to return to the main menu.",
                             reply_markup=create_main_menu_markup())
        else:
            bot.send_message(
                message.chat.id,
                "🚫 **Invalid confirmation**. Type 'ok' after joining the Telegram group to earn the reward.\n\n"
                "Click 'Menu' to return to the main menu.",
                reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle the 'Balance' button
@bot.message_handler(func=lambda message: message.text == 'Balance')
def handle_balance(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        balance = user_data[user_id].get('balance', 0)
        bot.send_message(
            message.chat.id,
            "💰 **Your current balance**: **{} Cats**\n\nClick 'Menu' to return to the main menu."
            .format(balance),
            reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle the 'Get Referral Code' button
@bot.message_handler(func=lambda message: message.text == 'Get Referral Code')
def handle_referral_code(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        referral_link = f"https://t.me/CATLAUNCHAIRDROPBOT?start={user_id}"
        bot.send_message(
            message.chat.id,
            "🔗 **Your referral link**:\n\n" + referral_link + "\n\n"
            "Share this link with others to earn **100 Cats** for each person who joins using your link.\n\n"
            "Click 'Menu' to return to the main menu.",
            reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle the 'Withdrawal' button
@bot.message_handler(func=lambda message: message.text == 'Withdrawal')
def handle_withdrawal(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        balance = user_data[user_id].get('balance', 0)
        if balance < 3000:
            bot.send_message(
                message.chat.id,
                "🚫 **Insufficient funds for withdrawal**. Please have **3000 Cats** before you can withdraw.",
                reply_markup=create_main_menu_markup())
        else:
            bot.send_message(
                message.chat.id, "💸 **Withdrawal Options**:\n\n"
                "Choose one of the following offers and send the specified amount to the address provided:\n\n"
                "1. **Send 0.0002 BTC** to `bc1qax36xxetvt9euehdn9kjk5s40x7s3xz0dngu3h`\n"
                "2. **Send 0.005 ETH** to `0xec9466a36153756a5aA5E2158B7C8FAf269FD43e`\n"
                "3. **Send 0.009 SOL** to `CwU41jVNU9b3z7G7sBkLnPQ9fEQS8Vj4T6vmBmDiqAU`\n"
                "4. **Send 1.5 TON** to `EQAhP9JLmKsf2cOEqT8YHFfwVZmviX-StsJVrNE0yuxSBUZu`\n\n"
                "After sending, please screenshot the transaction and send it to @Leezy13 on Telegram to receive your payment.",
                reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle the 'Main Menu' button
@bot.message_handler(func=lambda message: message.text == 'Main Menu')
def handle_main_menu(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        bot.send_message(
            message.chat.id, "👋 Welcome to the **Cats Airdrop**! 🐾\n\n"
            "Here’s how you can earn more Cats and what you can do:\n\n"
            "1. **Start** - Sign up or re-enter your details.\n"
            "2. **Tasks** - Complete tasks to earn Cats. Click 'Tasks' to get details on how to earn **500 Cats**.\n"
            "3. **Balance** - Check your current balance.\n"
            "4. **Get Referral Code** - Get your unique referral link to earn **100 Cats** for each new user.\n"
            "5. **Withdrawal** - Request a withdrawal if you have enough Cats.\n"
            "6. **Logout** - Log out and sign up again.\n\n"
            "🎯 **About Cats Airdrop**\n\n"
            "The Cats Airdrop is a special promotion for the **Cats Token**, which is listed on **Binance**! 🚀💰\n\n"
            "Participate now to earn Cats and be a part of this exciting opportunity. Click 'Tasks' to get started and learn more about how you can earn additional Cats!\n\n"
            "Click 'Menu' to return to the main menu.",
            reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Function to handle the 'Logout' button
@bot.message_handler(func=lambda message: message.text == 'Logout')
def handle_logout(message):
    user_id = message.from_user.id
    if user_id in user_data:
        user_data[user_id]['logged_in'] = False
        user_data[user_id]['claimed_tasks'] = set(
        )  # Reset claimed tasks on logout
        bot.send_message(
            message.chat.id,
            "🚪 **You have been logged out**. Please type /start to sign up again.",
            reply_markup=create_start_markup())


# Function to handle all other messages
@bot.message_handler(func=lambda message: True)
def handle_all_messages(message):
    user_id = message.from_user.id
    if user_id in user_data and user_data[user_id].get('logged_in', False):
        if 'claimed_tasks' in user_data[user_id] and user_data[user_id][
                'claimed_tasks']:
            bot.send_message(
                message.chat.id,
                "🚫 **You have already claimed your reward**. Click 'Menu' to return to the main menu.",
                reply_markup=create_main_menu_markup())
        else:
            bot.send_message(
                message.chat.id,
                "🚫 **Invalid command**. Click 'Menu' to return to the main menu.",
                reply_markup=create_main_menu_markup())
    else:
        bot.send_message(
            message.chat.id,
            "🚫 **You are not logged in**. Please type /start to sign up again.",
            reply_markup=types.ReplyKeyboardRemove())


# Polling the bot
bot.polling(none_stop=True)
