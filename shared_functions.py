from googletrans import Translator
import sqlite3
import telebot
from config import *
# Создаем объект для перевода текста
translator = Translator()

# Токен бота
bot = telebot.TeleBot(telegram_bot_token)


# Функция translate_to_user_language переводит текст на нужный язык
def translate_to_user_language(text, lang_code):
    if lang_code is None:
        pass
    # Переводим текст на язык пользователя с помощью Google Translate
    translation = translator.translate(text, dest=lang_code)
    translated_text = translation.text if translation.text else "Извините, перевод недоступен или произошла ошибка."
    return translated_text


# Увеличение количества токенов пользователя
def add_tokens(username, num_tokens):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()

    c.execute('''UPDATE users SET tokens = tokens + ? WHERE username = ?''', (num_tokens, username))

    conn.commit()
    conn.close()