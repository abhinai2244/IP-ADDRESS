import requests
from telebot import types
import telebot

# Replace this with your actual token
token = '7063668791:AAG89SDw8zccqfQgMcqtMPbYlCmLxvUWpqo'  # Replace with your bot token
bot = telebot.TeleBot(token)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, 'Send Your IP\nIPv6 address example: 2001:0db8:85a3:0000:0000:8a2e:0370:7334')

@bot.message_handler(func=lambda m: True)
def handle_message(message):
    user_name = message.from_user.first_name
    button = types.InlineKeyboardButton(text='Owner', url="https://t.me/Hmm_Smokie")
    markup = types.InlineKeyboardMarkup()
    markup.add(button)

    ip_address = message.text.strip()
    url = f'https://api.ip2location.io/?key=94C3D293714027465EBC944AFA3786A1&ip={ip_address}'

    try:
        response = requests.get(url)
        if response.status_code != 200:
            raise ValueError(f"API returned status code {response.status_code}")
        
        data = response.json()
        
        # Validate response data
        if not data or 'country_code' not in data:
            bot.reply_to(message, "Invalid IP address or unable to fetch details. Please try again.", reply_markup=markup)
            return

        # Extract fields with default values if missing
        ip = data.get("ip", "N/A")
        country_code = data.get("country_code", "N/A")
        country_name = data.get("country_name", "N/A")
        region_name = data.get("region_name", "N/A")
        city_name = data.get("city_name", "N/A")
        latitude = data.get("latitude", "N/A")
        longitude = data.get("longitude", "N/A")
        zip_code = data.get("zip_code", "N/A")
        time_zone = data.get("time_zone", "N/A")
        asn = data.get("asn", "N/A")
        as_name = data.get("as", "N/A")
        is_proxy = data.get("is_proxy", "N/A")

        # Format the message
        message_text = f"""IP: {ip}
Country Code: {country_code}
Country: {country_name}
Region: {region_name}
City: {city_name}
Latitude: {latitude}
Longitude: {longitude}
ZIP Code: {zip_code}
Time Zone: {time_zone}
ASN: {asn}
AS: {as_name}
Proxy: {is_proxy}

Developed by: """
        
        bot.reply_to(message, message_text, reply_markup=markup)
    except ValueError as ve:
        bot.reply_to(message, f"Error: {ve}", reply_markup=markup)
    except Exception as e:
        bot.reply_to(message, f"An unexpected error occurred: {e}", reply_markup=markup)

print('Bot is running...')
bot.infinity_polling()
