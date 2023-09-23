from os import listdir
from telebot import types
from config import *
from random import choice
import telebot
from shared_functions import *
from game_words import *
import sqlite3
import json

# Токен бота
bot = telebot.TeleBot(telegram_bot_token)

answer = ''
level = ''
game_active = True
index_question = 0
count_cor = 0
count_fal = 0
delete = 0
delete_great = 0
cheker = False
cheker2 = False


# Добавляем в базу данных уровень немецкого языка у пользователя
def add_level(username, lvl):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()

    c.execute('''UPDATE users SET level = ? WHERE username = ?''', (lvl, username))

    conn.commit()
    conn.close()


# Отсылаем доступные темы для пользователя на информация на темы, (версия: стандарт)
def make_themes_key_standart(message, choosed_lang):
    themes_markup = types.InlineKeyboardMarkup(row_width=3)
    names_themes = listdir('German_Helper/standart_version/Information_themes')
    list_buttons = []

    for name in names_themes:
        list_buttons.append(types.InlineKeyboardButton(name + choice(emojis), callback_data=name))

    themes_markup.add(*list_buttons)
    bot.send_message(message.chat.id, translate_to_user_language('Твои доступные темы:', choosed_lang),
                     reply_markup=themes_markup)


# Отсылаем доступные темы для пользователя на информация на темы, (версия: vip)
def make_themes_key_vip(message, choosed_lang):
    themes_markup = types.InlineKeyboardMarkup(row_width=3)
    names_themes = listdir('German_Helper/vip version/themes_information')
    list_buttons = []

    for name in names_themes:
        list_buttons.append(types.InlineKeyboardButton(name + choice(emojis), callback_data=name))

    themes_markup.add(*list_buttons)
    bot.send_message(message.chat.id, translate_to_user_language('Твои доступные темы:', choosed_lang),
                     reply_markup=themes_markup)


# Создаем ReplyKeyboardMarkup.
def create_replay_keyboard(lang_code, buttons_dict, buttons_dict2):
    # Создаем клавиатуру с переведенными кнопками
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for button_key, button_text in buttons_dict.items():
        translated_text = buttons_dict2[lang_code][button_key]
        keyboard.add(types.KeyboardButton(translated_text.capitalize()))
    return keyboard


# Добавляем нужные ReplyKeyboardMarkup.
def get_language_keyboard():
    # Создаем клавиатуру с доступными языками
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    for lang_name in AVAILABLE_LANGUAGES.values():
        markup.add(types.KeyboardButton(lang_name))
    return markup


# Отсылаем доступные темы для пользователя на рабочие листы, (версия: vip)
def make_work_sheets_vip(message, choosed_lang):
    sheets_markup = types.InlineKeyboardMarkup(row_width=3)
    names_sheets = listdir('German_Helper/vip version/sheets_work')
    list_buttons = []

    for name in names_sheets:
        list_buttons.append(types.InlineKeyboardButton(name + choice(emojis), callback_data=name))

    sheets_markup.add(*list_buttons)
    bot.send_message(message.chat.id, translate_to_user_language('Твои доступные темы:', choosed_lang),
                     reply_markup=sheets_markup)


# Отсылаем доступные темы для пользователя на рабочие листы, (версия: стандарт)
def make_work_sheets_standart(message, choosed_lang):
    sheets_markup = types.InlineKeyboardMarkup(row_width=3)
    names_sheets = listdir('German_Helper/standart_version/work_sheets')
    list_buttons = []

    for name in names_sheets:
        list_buttons.append(types.InlineKeyboardButton(name + choice(emojis), callback_data=name))

    sheets_markup.add(*list_buttons)
    bot.send_message(message.chat.id, translate_to_user_language('Твои доступные темы:', choosed_lang),
                     reply_markup=sheets_markup)


# Извлекаем из директорий и файлов аудио, фото, описание и документ
def send_info_or_worksheet(section, names_themes_list, callback, names_sheets):
    info_files = ''
    names_themes_ = ''
    if section == 'information':
        for name in listdir(names_themes_list):
            if callback.data == name:
                if callback.data in listdir(names_themes_standart):
                    info_files = listdir(f'{names_themes_standart}/{name}')
                    names_themes_ = names_themes_standart
                elif callback.data in listdir(names_themes_vip):
                    names_themes_ = names_themes_vip
                    info_files = listdir(f'{names_themes_vip}/{name}')
                photo_caption = ""
                for file in info_files:
                    if 'jpg' in file or 'png' in file:
                        with open(f'{names_themes_}/{name}/{file}', 'rb') as f:
                            photo = f.read()
                            bot.send_photo(callback.message.chat.id, photo, caption=photo_caption, parse_mode='HTML')
                    elif 'txt' in file:
                        with open(f'{names_themes_}/{name}/{file}',
                                  encoding='utf-8') as fl:
                            description = fl.read()

                            photo_caption = description
                    elif 'mp3' in file:
                        with open(f'{names_themes_}/{name}/{file}', 'rb') as f:
                            audio = f.read()
                            bot.send_audio(callback.message.chat.id, audio)
    elif section == 'worksheets':
        for name in listdir(names_sheets_standart):
            if callback.data == name:
                sheets_file = listdir(f'{names_sheets}/{name}')
                for name_sheet in sheets_file:
                    with open(f'{names_sheets}/{name}/{name_sheet}', 'rb') as f:
                        document = f.read()
                        bot.send_document(callback.message.chat.id, document)


# Отправляем пользователю информацию на темы или рабочие листы.
def open_information_or_worksheet(callback, version, names_t_list, names_s_list, names_t_vip_list, names_s_vip_list,
                                  section):
    if version == 'default':
        send_info_or_worksheet(section, names_t_list, callback, names_s_list)
    elif version == 'vip':
        send_info_or_worksheet(section, names_t_vip_list, callback, names_s_vip_list)


# Узнаем нужный уровень пользователя
def make_lvl_key(callback, chossed_lang, user_level):
    key = types.InlineKeyboardMarkup(row_width=1)

    spacial_button = types.InlineKeyboardButton(translate_to_user_language('Мой уровень', chossed_lang),
                                                callback_data=user_level.upper() + '.txt')
    if callback.data == 'дя':
        lvl_names = listdir("German_Helper/игра 'как на Deutsch'")
        list_buttons = []
        for name in lvl_names:
            list_buttons.append(types.InlineKeyboardButton(name.replace('.txt', ''), callback_data=name))

        key.add(*list_buttons).add(spacial_button)

        bot.send_message(callback.message.chat.id, translate_to_user_language('Выбери твой уровень:', chossed_lang),
                         reply_markup=key)


# Сппрашиваем у пользователя готов ли он
def ready_user(message, choosed_lang, call_yes, call_no):
    key = types.InlineKeyboardMarkup(row_width=1)

    yes = types.InlineKeyboardButton(translate_to_user_language('Да', choosed_lang) + '🟢', callback_data=call_yes)
    no = types.InlineKeyboardButton(translate_to_user_language('Не хочу', choosed_lang), callback_data=call_no)
    key.add(yes)
    key.add(no)

    bot.send_message(message.chat.id, translate_to_user_language('Ты готов начать игру?', choosed_lang),
                     reply_markup=key)


# Из словарей возвращаем слово на немецком и на русском
def rand_words(dict1):
    global answer
    ra_dict = dict1
    random_key_ = choice(list(ra_dict.keys()))
    random_word_ = ra_dict.get(random_key_)
    answer = random_key_

    return random_key_, random_word_


# Возвращаем рандомное слово на немецком языке.
def make_random_game_words(lvl):
    global level, answer
    if lvl == 'A1.txt':
        level = 'A1'
        return rand_words(german_a1_to_russian)

    elif lvl == 'A2.txt':
        level = 'A2'
        return rand_words(german_a2_to_russian)

    elif lvl == 'B1.txt':
        level = 'B1'
        return rand_words(german_b1_to_russian)


# Отсылаем не правильный ответ, (что пользователь ответил не правильно)
def send_false_mes(ans, message, lang):
    cor_answer = f'"{ans}"\n'
    word = make_random_game_words('A1.txt')
    bot.send_message(message.chat.id, translate_to_user_language('''❌К сожалению, это не правильный ответ,
            правильно будет:''', lang) + cor_answer +
                     translate_to_user_language(say_task + f'"{word[-1].lower()}"', lang))


# Отсылаем правильный ответ, (что пользователь ответил правильно)
def send_correct_mes(name, tok, message, lang):
    token = f'+{tok} tokens🤑\n'
    add_tokens(name, tok)
    word = make_random_game_words('A1.txt')
    bot.send_message(message.chat.id, translate_to_user_language(correct_answer + token + say_task +
                                                                 f'"{word[-1].lower()}"',
                                                                 lang))


# Функция для отправки пользоватею первое слово на нужном языке
def send_first_game_word(name_dict, callback, lang):
    word = make_random_game_words(name_dict)
    bot.send_message(callback.message.chat.id, translate_to_user_language(say_task + f'"{word[-1]}"', lang))


# Отсылаем первое слово на языке выбранным пользователем
def send_random_game_words(callback, lang):
    if callback.data == 'A1.txt':
        send_first_game_word('A1.txt', callback, lang)

    elif callback.data == 'A2.txt':
        send_first_game_word('A2.txt', callback, lang)

    elif callback.data == 'B1.txt':
        send_first_game_word('B1.txt', callback, lang)


def correct_game_answers(message, lang, name):
    global answer, level, game_active

    if not game_active:
        return

        # Если игрок хочет остановить игру
    if message.text.strip().lower() == "/stop_game":
        bot.send_message(message.chat.id, translate_to_user_language("The game has been stopped.", lang))

        game_active = False
        return

    if message.text.lower() == answer.lower():
        if level == 'A1':
            send_correct_mes(name, 1, message, lang)
        elif level == 'A2':
            send_correct_mes(name, 2, message, lang)
        elif level == 'B1':
            send_correct_mes(name, 3, message, lang)

    else:
        if level == 'A1':
            send_false_mes(answer, message, lang)
        elif level == 'A2':
            send_false_mes(answer, message, lang)
        elif level == 'B1':
            send_false_mes(answer, message, lang)


# Создание базы данных и таблиц
def create_tables():
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()

    c.execute('''CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY,
                    username TEXT NOT NULL UNIQUE,
                    version TEXT NOT NULL,
                    tokens INTEGER NOT NULL DEFAULT 0,
                    level TEXT
                )''')

    conn.commit()
    conn.close()


# Обработка message 'Меню📋'
def handle_menu_func(message, user_lang_code, answer_version, tokens, username):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()

    if message.text == translate_to_user_language('Меню📋', user_lang_code) or message.text == 'Меню📋':
        bot.send_message(message.chat.id, f"""<b>{translate_to_user_language('Список команд:', user_lang_code)}</b>
        /help - {translate_to_user_language('Посмотреть все команды пользователя', user_lang_code)}
        /token - {translate_to_user_language('Посмотреть количество токенов', user_lang_code)}
        /version -{translate_to_user_language('Посмотреть версию', user_lang_code)}
        /start - {translate_to_user_language('Старт бота', user_lang_code)}""",
                         parse_mode='HTML')

    elif message.text == translate_to_user_language('Версия', user_lang_code) + "😎":
        bot.send_message(message.chat.id, answer_version)

    elif message.text == translate_to_user_language('Токены', user_lang_code) + '🤑' or message.text == 'Токени🤑':
        c.execute('''SELECT tokens FROM users WHERE username = ?''', (username,))
        user_tokens = c.fetchone()
        conn.commit()

        for token in user_tokens:
            user_tokens = token

        bot.send_message(message.chat.id, translate_to_user_language(f'Ваше количетство токенов🤑:\n{user_tokens}',
                                                                     user_lang_code))

    elif message.text == translate_to_user_language('Купить версию🌕', user_lang_code):
        if tokens >= 1000:
            c.execute('''UPDATE users SET version= ? WHERE username= ?''', ('vip', username))
            conn.commit()
            bot.send_message(message.chat.id, translate_to_user_language(buy_vip, user_lang_code), parse_mode='HTML')

        else:
            bot.send_message(message.chat.id, translate_to_user_language('Вам нужно иметь не менее 1000 токенов!',
                                                                         user_lang_code))


# Обработка message 'Вернуться назад◀️'
def handle_return(message, choosed_lang, creat_inline_key_yes_no, AVAILABLE_BUTTONS, BUTTONS_TRANSLATIONS, markup2):
    if message.text == translate_to_user_language('Вернуться назад◀️', choosed_lang):
        menu_markup2 = create_replay_keyboard(choosed_lang, AVAILABLE_BUTTONS, BUTTONS_TRANSLATIONS)
        bot.send_message(message.chat.id, translate_to_user_language('Это твоя меню клавиатура:', choosed_lang),
                         reply_markup=menu_markup2)
        creat_inline_key_yes_no(message, markup2, choosed_lang, 'yes', 'no', 'Вернуться вперед▶️')


# Обработка message 'Как на deutsch🇩🇪?'
def handle_deutsch(message, choosed_lang, regel_game, name):
    if message.text == 'Як на deutsch?🇩🇪' or message.text == 'Как на deutsch🇩🇪?'\
            or message.text == 'How on deutsch?🇩🇪':

        bot.send_message(message.chat.id, translate_to_user_language(regel_game, choosed_lang), parse_mode='HTML')
        ready_user(message, choosed_lang, 'дя', 'no')

    correct_game_answers(message, choosed_lang, name)


# Обрабатываем message 'Пройти тест🧑‍💻'
def handle_test(message, user_lang_code):
    global delete

    if message.text == translate_to_user_language('Пройти тест🧑‍💻', user_lang_code):
        bot.send_message(message.chat.id, translate_to_user_language(regel_test, user_lang_code) + ' 2️⃣0️⃣ ' +
                         translate_to_user_language(''' вопросов.
Удачи в прохождении!😀''', user_lang_code), parse_mode='HTML')

        ready_user(message, user_lang_code, 'go', 'no')


# Открывам JSON файл с вопросами и ответами для теста.
def open_test():
    with open('test.json', encoding='utf-8') as file:
        test_q_a = json.load(file)
    return test_q_a


def send_first_test_task(callback):
    global index_question, delete, cheker
    _test_ = open_test()

    answers = _test_['questions'][index_question]['answers']
    question = _test_['questions'][index_question]['question']

    if callback.data == 'go' and not index_question:
        markup = telebot.types.InlineKeyboardMarkup()
        for answer in answers:
            button = telebot.types.InlineKeyboardButton(text=answer, callback_data=answer)
            markup.add(button)

        delete = bot.send_message(callback.message.chat.id, question, reply_markup=markup).message_id
        cheker = True


def mes_end_test(callback, user_lang, username, Tmin, Tmax, level, great_level):
    global count_cor

    if Tmin <= count_cor <= Tmax:
        add_level(username, level)
        bot.send_message(callback.message.chat.id, translate_to_user_language(great_level, user_lang),
                         parse_mode='HTML')


def end_test(callback, user_lang, username):
    global index_question
    if index_question >= 20:
        mes_end_test(callback, user_lang, username, 1, 5, 'A1', level_a1)
        mes_end_test(callback, user_lang, username, 6, 10, 'A1', level_a1)
        mes_end_test(callback, user_lang, username, 11, 15, 'A2', level_a2)
        mes_end_test(callback, user_lang, username, 16, 20, 'B1', level_b1)

    index_question = 0


def make_tasks_keyboard(callback, question, answers):
    global delete
    markup = telebot.types.InlineKeyboardMarkup()
    for answer in answers:
        button = telebot.types.InlineKeyboardButton(text=answer, callback_data=answer)
        markup.add(button)

    delete = bot.send_message(callback.message.chat.id, question, reply_markup=markup).message_id


def send_test(callback, user_lang_code, username):
    global index_question, count_cor, count_fal, delete, delete_great, cheker
    _test_ = open_test()
    correct_task_answer = _test_['questions'][index_question]['correct_answer']

    try:
        try:
            if callback.data == correct_task_answer and cheker:
                bot.delete_message(callback.message.chat.id, delete)
                index_question += 1

                count_cor += 1

                if not delete_great:
                    pass
                else:
                    bot.delete_message(callback.message.chat.id, delete_great)
                answers = _test_['questions'][index_question]['answers']
                question = _test_['questions'][index_question]['question']
                rand_great = choice(random_great_words)
                correct_task_answer = _test_['questions'][index_question]['correct_answer']

                delete_great = bot.send_message(callback.message.chat.id,
                                                translate_to_user_language(f'''🟢{rand_great}'
    <i>Количество правильных ответов: {count_cor}.
    Количество не правильных ответов: {count_fal}.
    Количество ответов: {index_question}.</i>
    Следующее задание:''', user_lang_code), parse_mode='HTML').message_id

                markup = telebot.types.InlineKeyboardMarkup()
                for answer in answers:
                    button = telebot.types.InlineKeyboardButton(text=answer, callback_data=answer)
                    markup.add(button)

                delete = bot.send_message(callback.message.chat.id, question, reply_markup=markup).message_id

            elif callback.data != correct_task_answer and cheker and delete and delete_great:
                bot.delete_message(callback.message.chat.id, delete)
                index_question += 1

                count_fal += 1

                if not delete_great:
                    pass
                else:
                    bot.delete_message(callback.message.chat.id, delete_great)
                    answers = _test_['questions'][index_question]['answers']
                    question = _test_['questions'][index_question]['question']
                    rand_great = choice(random_false_words)
                    correct_task_answer = _test_['questions'][index_question]['correct_answer']

                    delete_great = bot.send_message(callback.message.chat.id,
                                                    translate_to_user_language(f'''🔴{rand_great}
        <i>Количество правильных ответов: {count_cor}.
        Количество не правильных ответов: {count_fal}.
        Количество ответов: {index_question}.</i>
        Следующее задание:''', user_lang_code), parse_mode='HTML').message_id

                    markup = telebot.types.InlineKeyboardMarkup()
                    for answer in answers:
                        button = telebot.types.InlineKeyboardButton(text=answer, callback_data=answer)
                        markup.add(button)

                    delete = bot.send_message(callback.message.chat.id, question, reply_markup=markup).message_id
        except telebot.apihelper.ApiTelegramException:
            pass
    except IndexError:
        end_test(callback, user_lang_code, username)



