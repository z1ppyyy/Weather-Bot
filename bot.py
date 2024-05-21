import telebot
from config import TOKEN, API_KEY  # Assuming your API key is stored in config.py
import requests

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Welcome to the Weather Bot ☀️\nType the name of the city you're interested in:")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    user_input = message.text.title()

    weather_data = requests.get(
    f"http://api.openweathermap.org/data/2.5/weather?q={user_input}&appid={API_KEY}")

    if weather_data.json()['cod'] == '404':
        bot.send_message(message.chat.id, "City not found")
    else:
        # Extract weather information
        weather = weather_data.json()['weather'][0]['description']
        temp = round(weather_data.json()['main']['temp'])
        c = round(temp - 273.15)
        feels_like = round(weather_data.json()['main']['feels_like']) - 273.15
        humidity = weather_data.json()['main']['humidity']
        wind_speed = weather_data.json()['wind']['speed']  # Assuming m/s unit

        # Formatted weather output
        weather_message = f"""City: {user_input}
Current Temperature: {c} °C
Feels Like: {round(feels_like)} °C
Weather: {weather}
Humidity: {humidity}%
Wind Speed: {wind_speed} m/s"""

        bot.send_message(message.chat.id, weather_message)

# Run the bot
bot.polling()