# -*- coding: utf-8 -*-
import redis
import os
import telebot
# import some_api_lib
# import ...

# Example of your code beginning
#           Config vars
token = os.environ['TELEGRAM_TOKEN']
some_api_token = os.environ['SOME_API_TOKEN']
#             ...

# If you use redis, install this add-on https://elements.heroku.com/addons/heroku-redis
r = redis.from_url(os.environ.get("REDIS_URL"))

#       Your bot code below
# bot = telebot.TeleBot(token)
# some_api = some_api_lib.connect(some_api_token)
#              ...
# -*- coding: utf8 -*-
import telebot
from telebot import types

bot = telebot.TeleBot(token)

print(bot.get_me())

def log(message, answer):
    print("\n -----")
    from datetime import datetime
    print(datetime.now())
    print("Сообщение от {0} {1} (id = {2}), username - {4} \n Текст - {3}." .format(message.from_user.first_name,
                                                                 message.from_user.last_name,
                                                                 str(message.from_user.id),
                                                                 message.text,
                                                                 message.from_user.username))
    print(answer)

@bot.message_handler(commands=["start"])
def start(message):
    sent = bot.send_message(message.chat.id, "Как тебя зовут?")
    bot.register_next_step_handler(sent, hello)

def hello(message):
    bot.send_message(message.chat.id, "Привет, {name}. Рад тебя видеть. Пожалуйста, отправте мне свой номер для этого есть команда /phone".format(name=message.text))

@bot.message_handler(commands=["phone"])
def phone(message):
    user_markup = types.ReplyKeyboardMarkup(row_width=1, resize_keyboard=True, one_time_keyboard=True)
    button_phone = types.KeyboardButton(text="Отправить номер телефона", request_contact=True)
    user_markup.add(button_phone)
    msg = bot.send_message(message.chat.id, "Согласны ли вы предоставить ваш номер телефона для регистрации в системе?", reply_markup=user_markup)
    bot.register_next_step_handler(msg, main_menu)

@bot.message_handler()
def main_menu(message):
    user_markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    user_markup.add(*[types.KeyboardButton(name) for name in ["🚕 Заказать Такси"]])
    user_markup.add(*[types.KeyboardButton(name) for name in ["🚚 Доставка", "📣 Новости"]])
    user_markup.add(*[types.KeyboardButton(name) for name in ["📋 Тарифы", "📞 Контакты"]])
    user_markup.add(*[types.KeyboardButton(name) for name in ["⚙ Настройки"]])
    mess = bot.send_message(message.chat.id, "Добро пожаловать", reply_markup=user_markup)
    bot.register_next_step_handler(mess, menu)

@bot.message_handler("text")
def menu(message):
    if message.text == "🚕 Заказать Такси":
        t = "Отправте адрес или координаты"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        button_loca = types.KeyboardButton(text="🌐 Определить местоположение", request_location=True)
        keyboard.add(button_loca)
        keyboard.add(*[types.KeyboardButton(name) for name in ["⌚️Сейчась", "📆 На когда"]])
        keyboard.add(*[types.KeyboardButton(name) for name in ["⏪ Назад ⏪"]])
        bot.send_message(message.chat.id, t,  parse_mode="HTML", reply_markup=keyboard)

    if message.text == "📣 Новости":
        j = "Оставайтесь в курсе новостей и акций компании <b>UNI TAXI</b>\n👉 https://t.me/unitaxiofficial"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["⏪ Назад ⏪"]])
        bot.send_message(message.chat.id, j, parse_mode="HTML", reply_markup=keyboard)

    if message.text == "⚙ Настройки":
        j = "<b>UNI TAXI</b>\n\nпока найстройки не настроены :)"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["⏪ Назад ⏪"]])
        bot.send_message(message.chat.id, j, parse_mode="HTML", reply_markup=keyboard)

    if message.text == "📞 Контакты":
        k = "<b>UNI TAXI</b>\n\n<b>📞 Телефоны диспетчерской:</b>\n+99871 2001771\n+99871 2007117\n\n<b>📞 Приём водителей:</b>\n+99890 9110220\n"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["⏪ Назад ⏪"]])
        bot.send_message(message.chat.id, k, parse_mode="HTML", reply_markup=keyboard)

    if message.text == "📋 Тарифы":
        t = "<b>Эконом: Maniz, Spark, Nexia</b>\nСтавка: 6000 сум/3км, ожидание/5мин\nДалее: 1200 сум/км, ожидание мин/400 сум\nЗагород: 1500 сум/км\n\n<b>Комфорт: Cobalt, Lacetti, Gentra</b>\nСтавка: 8000 сум/3км, ожидание/5мин\nДалее: 1400 сум/км, ожидание мин/500 сум\nЗагород: 1700 сум/км\n\n<b>Комфорт: Epica, Malibu, Captiva</b>\nСтавка: 12000 сум/3км, ожидание/5мин\nДалее: 1800 сум/км, ожидание мин/500 сум\nЗагород: 2200 сум/км"
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(*[types.KeyboardButton(name) for name in ["⏪ Назад ⏪"]])
        bot.send_message(message.chat.id, t, parse_mode="HTML", reply_markup=keyboard)

    if message.text == "⏪ Назад ⏪":
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(*[types.KeyboardButton(name) for name in ["🚕 Заказать Такси "]])
        markup.add(*[types.KeyboardButton(name) for name in ["📋 Тарифы", "📞 Контакты"]])
        markup.add(*[types.KeyboardButton(name) for name in ["⚙️Настройки"]])

if __name__ == '__main__':
    bot.polling(none_stop=True)
