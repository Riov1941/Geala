import os
import telebot
import time
from threading import Thread
from telebot import types

TOKEN = 'TOKEN'
bot = telebot.TeleBot(TOKEN)

def rest_timer(chat_id, seconds):
    time.sleep(seconds)
    minutes = seconds // 60
    bot.send_message(chat_id, f"⏰ Время вышло. Твои {minutes} мин. отдыха закончились. Пора на следующий подход.")

# Приветствие и создание кнопок
@bot.message_handler(commands=['start'])
def start_message(message):
    # Создаем клавиатуру
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    
    # Создаем три кнопки
    btn_1 = types.KeyboardButton('⏱ 1 мин')
    btn_15 = types.KeyboardButton('⏱ 1.5 мин')
    btn_2 = types.KeyboardButton('⏱ 2 мин')
    
    # Добавляем их на клавиатуру (можно в один ряд или в разные)
    # markup.add(btn_1, btn_15, btn_2) # Если хочешь в один ряд
    markup.row(btn_1, btn_15) # 1 и 1.5 в один ряд
    markup.row(btn_2)         # 2 минуты во второй ряд
    
    bot.send_message(
        message.chat.id, 
        'Здарова, пора ебашить. Я помогу. Сразу после подхода можешь выбрать время отдыха снизу:', 
        reply_markup=markup
    )

# Обработчик для всех трех кнопок
@bot.message_handler(func=lambda message: message.text in ['⏱ 1 мин', '⏱ 1.5 мин', '⏱ 2 мин'])
def timer_message(message):
    text = message.text
    
    # Определяем, сколько секунд ждать
    if text == '⏱ 1 мин':
        seconds = 60
    elif text == '⏱ 1.5 мин':
        seconds = 90
    else:
        seconds = 120
        
    bot.send_message(message.chat.id, f"⏳ Отдых начался. У тебя {text[2:]}.")
    
    # Запускаем таймер в фоне
    thread = Thread(target=rest_timer, args=(message.chat.id, seconds))
    thread.start()

# Реакция на любой другой текст
@bot.message_handler(content_types=['text'])
def unknown_message(message):
    bot.send_message(message.chat.id, 'Жми /start, чтобы начать работать')

print('Работает...')
bot.infinity_polling()