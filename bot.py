import telebot
from telebot import types
from threading import Thread
from time import sleep
import schedule
from datetime import datetime
import pytz
import random

# === НАСТРОЙКИ ===
TOKEN = 'твой_токен'

# --- фразы ---
pause_tips = [
    "Сделай пару глубоких вдохов 💨",
    "Посмотри в окно. Да, просто так ☁️",
    "Закрой глаза на минуту и ничего не делай 🧘",
]

stretch_tips = [
    "Потяни плечи назад и вверх 💪",
    "Пройди до кухни и обратно (без кофе!) 🚶",
    "Сделай пару наклонов или приседаний 🏃",
]

reminders = [
    "Небольшой перерыв = больше фокуса 💡",
    "Пора встать, размяться, а потом вернуться 🔄",
    "Ты молодец. А теперь сделай паузу ☕",
]

# --- инициализация ---
bot = telebot.TeleBot(TOKEN)
active_users = set()

# === ОБРАБОТКА КОМАНД И КНОПОК ===
@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('🧘 Отдохнуть', '🚶 Размяться')
    markup.add('🔁 Хочу напоминания', '❌ Хватит напоминаний')
    bot.send_message(message.chat.id, 'Привет! Я помогу тебе делать полезные перерывы 😊', reply_markup=markup)

@bot.message_handler(func=lambda msg: True)
def handle_button(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if text == '🧘 Отдохнуть':
        bot.send_message(user_id, random.choice(pause_tips))

    elif text == '🚶 Размяться':
        bot.send_message(user_id, random.choice(stretch_tips))

    elif text == '🔁 Хочу напоминания':
        active_users.add(user_id)
        bot.send_message(user_id, 'Буду напоминать тебе делать перерывы с 10 до 18 (МСК) каждый час ⏰')

    elif text == '❌ Хватит напоминаний':
        if user_id in active_users:
            active_users.remove(user_id)
            bot.send_message(user_id, 'Хорошо, не буду больше беспокоить 🙃')
        else:
            bot.send_message(user_id, 'У тебя и не были включены напоминания 🤔')

    else:
        bot.send_message(user_id, 'Я пока понимаю только кнопки 🙈 Пожалуйста, нажимай на них ниже 👇')

# === АВТОМАТИЧЕСКАЯ РАССЫЛКА ===
def send_reminders():
    now = datetime.now(pytz.timezone('Europe/Moscow'))
    if 10 <= now.hour <= 18:
        for user_id in active_users:
            try:
                bot.send_message(user_id, random.choice(reminders))
            except:
                pass  # если пользователь заблокировал бота — не падаем

schedule.every().hour.at(":00").do(send_reminders)

def schedule_worker():
    while True:
        schedule.run_pending()
        sleep(30)

# === ЗАПУСК ===
if __name__ == '__main__':
    Thread(target=schedule_worker).start()
    bot.infinity_polling()
