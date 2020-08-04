import telebot
import requests

token = "1309890746:AAEljMVb1VdQppBAqAktqfCQk2PcXindBRw"
bot = telebot.TeleBot(token)

@bot.message_handler(regexp="hello")
def say_hello(message):
    print(message)
    bot.send_message(message.chat.id, f'И тебе привет, {message.from_user.first_name}!')

@bot.message_handler(commands=["start"])
def start_bot(message):
    msg = "Курс валют = /valute \nПогода - /weather"
    bot.send_message(message.chat.id, msg)

@bot.message_handler(regexp='Стикер')
def send_sticker(message):
    id = 'asdfasdfasdfsdf'
    bot.send_sticker(message.chat.id, id)

@bot.message_handler(commands=["valute"])
def get_valute(message):
    url = "https://www.cbr-xml-daily.ru/daily_json.js"
    currency = requests.get(url).json()
    usd = currency['Valute']['USD']['Value']
    eur = currency['Valute']['EUR']['Value']
    bot.send_message(message.chat.id, f"Доллар: {usd}, Евро: {eur}")

@bot.message_handler(commands=["weather"])
def get_city(message):
    msg = bot.send_message(message.chat.id, "Какой город?")
    bot.register_next_step_handler(msg, get_weather)

def get_weather(message):
    city = message.text
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid=3c476f22a5b257b9d84b96dbf18ad854"
    data = requests.get(url).json()
    bot.send_message(message.chat.id, f"{city} - {(data['main']['temp'] - 273.15) // 1}")

bot.polling()