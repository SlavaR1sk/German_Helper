import telebot
from telebot import types
import config
from config import *
from imp_funcs import *
from shared_functions import translate_to_user_language
import sqlite3
import json

# Здесь создается объект бота с использованием токена, который был импортирован из файла config.
bot = telebot.TeleBot(telegram_bot_token)

# Словарь для хранения выбранного языка каждого пользователя.
user_languages = {}

# Переменная для хранения выбранного языка пользователя.
choosed_lang = None

# Список для хранения идентификаторов сообщений, чтобы их можно было удалить позже.
ids_messages = []

name = None

username, version, tokens, level = None, None, None, None

section = None

# Вызываем функцию create_tables из imp_funcs.py, ряд 289, в которой будет создаваться нужная таблица
create_tables()


# Функция add_user используется для добавления новых пользователей
# в базу данных или получения информации о существующих пользователях.
# Если пользователь уже существует, возвращаются его данные.
def add_user(username, version):
    conn = sqlite3.connect('language_bot.db')
    c = conn.cursor()

    c.execute('''SELECT username, version, tokens, level FROM users WHERE username = ?''', (username,))
    existing_user = c.fetchone()
    if existing_user is None:
        try:
            c.execute('''INSERT INTO users (username, version) VALUES (?, ?)''', (username, version))
            conn.commit()
        except sqlite3.IntegrityError:
            pass
    else:
        # Возвращаем все поля существующего пользователя
        conn.close()
        return existing_user

    conn.commit()
    conn.close()


# Функция creat_inline_key_yes_no используется для создания клавиатуры с двумя вариантами ответа: "Да" и "Нет".
# Она также отправляет сообщение с этой клавиатурой и добавляет идентификатор сообщения в список ids_messages.
def creat_inline_key_yes_no(message, name_key, lang_code, call_yes, call_no, question):
    global ids_messages
    want_continue = question
    list_yes_no = [types.InlineKeyboardButton(translate_to_user_language('да✅', lang_code),
                                              callback_data=call_yes),
                   types.InlineKeyboardButton(translate_to_user_language('нет🔴', lang_code),
                                              callback_data=call_no)]
    name_key.add(*list_yes_no)
    mes = bot.send_message(message.chat.id, translate_to_user_language(want_continue, lang_code),
                            reply_markup=name_key, parse_mode='HTML').message_id

    # Берем айди сообщения и добавляем в список для дальнейшего удаления
    ids_messages.append(mes)


# Функция get_keyboard_markup используется для создания встроенной клавиатуры (inline keyboard markup)
# на основе данных из файла "test.json".
# Эта клавиатура будет использоваться для предоставления пользователю вариантов ответов на вопросы.
def get_keyboard_markup():
    with open('test.json', encoding='utf-8') as file:
        questions = json.load(file)['questions'][0]['answers']

    markup = telebot.types.InlineKeyboardMarkup()
    for answer in questions:
        button = telebot.types.InlineKeyboardButton(text=answer, callback_data=answer)
        markup.add(button)
    return markup


# Функция show_menu используется для отправки пользователю сообщения с клавиатурой и описанием.
def show_menu(message, keyboard, description):
    global ids_messages
    user_lang_code = user_languages.get(message.from_user.id)

    if not user_lang_code:
        pass
    else:
        # Если у пользователя уже выбран язык, покажем меню на этом языке

        mes = bot.send_message(message.chat.id, translate_to_user_language(description, user_lang_code),
                               reply_markup=keyboard).message_id

        # Берем айди сообщения и добавляем в список для дальнейшего удаления
        ids_messages.append(mes)


# Функция great_user отправляет приветствие пользователю, включая анимацию и текст меню.
def great_user(message):
    global ids_messages
    # Отправка приветствия, анимации и текста меню, переведенных на язык пользователя
    mes1 = bot.send_message(message.chat.id, translate_to_user_language(config.great,
                            user_languages[message.from_user.id]), parse_mode='HTML').message_id

    mes = bot.send_animation(message.chat.id, animation_id).message_id

    # Берем айди сообщения и добавляем в список для дальнейшего удаления
    ids_messages.append(mes1)


# Функция choose_lang отправляет сообщение с предложением выбрать язык для общения.
def choose_lang(message):
    global ids_messages
    mes = bot.send_message(message.chat.id, "Выберите язык, чтобы начать общение.",
                           reply_markup=get_language_keyboard()).message_id
    # Берем айди сообщения и добавляем в список для дальнейшего удаления
    ids_messages.append(mes)


# Функция show_menu_key используется для показа пользователю меню с клавиатурой и вопросом о продолжении.
def show_menu_key(message, language, markup):
    menu_markup = create_replay_keyboard(language, AVAILABLE_BUTTONS, BUTTONS_TRANSLATIONS)
    great_user(message)

    show_menu(message, menu_markup, 'Это твоя меню клавиатура:')
    creat_inline_key_yes_no(message, markup, language, 'yes', 'no', f'<b>Хотите ли вы продолжить?</b>')


# Обработчики команд, вызываемые пользователями. В зависимости от команды, отправляется соответствующее сообщение.
# Также выполняется добавление пользователя в базу данных.
@bot.message_handler(commands=['help', 'version', 'token', 'level'])
def list_commands(message):
    global version, username, tokens, level

    user_info = add_user(name, 'default')  # Здесь устанавливаем версию "default" при первом заходе

    try:
        username, version, tokens, level = user_info
    except TypeError:
        pass

    try:
        if message.text == '/help':
            bot.send_message(message.chat.id, config.list_commands, parse_mode='HTML')

        elif message.text == '/version':
            try:
                bot.send_message(message.chat.id, version)
            except telebot.apihelper.ApiTelegramException:
                bot.send_message(message.chat.id, '/start')
        elif message.text == '/token':
            bot.send_message(message.chat.id, f'{tokens} Tokens🤑')

        elif message.text == '/level':
            try:
                bot.send_message(message.chat.id, f'Level:{level}')
            except TypeError:
                bot.send_message(message.chat.id, 'level: None')

    except sqlite3.IntegrityError:
        bot.send_message(message.chat.id, '/start')


@bot.message_handler(commands=['start'])
def send_welcome(message):
    global name, ids_messages, username, version, tokens, user_languages, level

    name = message.from_user.first_name
    user_info = add_user(name, 'default')  # Здесь устанавливаем версию "default" при первом заходе

    try:
        username, version, tokens, level = user_info
    except TypeError:
        pass

    # Отправляем приветственное сообщение и клавиатуру с языками при вводе команды /start
    if message.text == '/start':
        mes = bot.send_message(message.chat.id, "Привет! Выберите язык на котором хотите общаться:",
                               reply_markup=get_language_keyboard()).message_id

        # Берем айди сообщения и добавляем в список для дальнейшего удаления
        ids_messages.append(mes)


# Обработчик текстовых сообщений. Здесь осуществляется обработка ввода пользователя.
@bot.message_handler(content_types=['text'])
def handle_message(message):
    global choosed_lang, ids_messages, name, username, version, tokens, section

    user_input = message.text.lower()
    user_lang_code = user_languages.get(message.from_user.id)
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup2 = types.InlineKeyboardMarkup(row_width=2)

    if user_lang_code:
        if user_input in [lang_name.lower() for lang_name in AVAILABLE_LANGUAGES.values()]:
            # Если пользователь уже выбрал язык, установите choosed_lang и отобразите меню.
            choosed_lang = user_lang_code
            show_menu_key(message, user_lang_code, markup)

    elif user_input in [lang_name.lower() for lang_name in AVAILABLE_LANGUAGES.values()]:
        # Если пользователь выбирает язык, обновите choosed_lang и отобразите меню.
        for lang_code, lang_name in AVAILABLE_LANGUAGES.items():
            if user_input == lang_name.lower() and user_input != '/start':
                user_languages[message.from_user.id] = lang_code
                user_lang_code = lang_code
                choosed_lang = user_lang_code

                show_menu_key(message, user_lang_code, markup)
                break

    if user_lang_code is None:
        return

    '''Вызываем функции которые обработывают message пользователя.'''
    handle_deutsch(message, user_lang_code, regel_game, name)

    try:
        answer_version = translate_to_user_language(f'{username}, Ваша версия:  ', choosed_lang) + version
        handle_menu_func(message, user_lang_code, answer_version, tokens, username)

    except TypeError:
        bot.send_message(message.chat.id, translate_to_user_language(f'{username}, Ваша версия:  ',
                                                                     choosed_lang) + 'default')

    handle_return(message, user_lang_code, creat_inline_key_yes_no, AVAILABLE_BUTTONS, BUTTONS_TRANSLATIONS, markup2)

    handle_test(message, user_lang_code)

    # Обрабываем messages Информация на темы и 'Рабочие листы📄'
    if message.text == translate_to_user_language('Информация на темы🤓', user_lang_code):
        print(version)
        section = 'information'
        if version == 'default':

            make_themes_key_standart(message, user_lang_code)
        elif version == 'vip':
            make_themes_key_vip(message, user_lang_code)

    elif message.text == translate_to_user_language('Рабочие листы📄', user_lang_code):
        section = 'worksheets'
        if version == 'default':

            make_work_sheets_standart(message, user_lang_code)
        elif version == 'vip':
            make_work_sheets_vip(message, user_lang_code)

    """Для теста платной версии"""
    #if message.text == '/get_tokens':
        #add_tokens(username, 1000)


# Обработчик колбэков (callback) - это ответы на действия пользователя, сделанные на inline клавиатуре.
@bot.callback_query_handler(func=lambda callback: True)
def callback_handler(callback):
    global ids_messages, choosed_lang, username, version, tokens, section, level

    if callback.data == 'yes':
        # Удаляем предыдущие сообщения
        for message_id in ids_messages:
            try:
                bot.delete_message(callback.message.chat.id, message_id)
            except telebot.apihelper.ApiTelegramException as e:
                # Если сообщение не может быть удалено, продолжаем без ошибки

                pass

        # Очищаем список идентификаторов сообщений после удаления
        ids_messages.clear()

        bot_func = create_replay_keyboard(choosed_lang, list_bot_function, list_bot_function2)
        bot_func.add(types.KeyboardButton(translate_to_user_language('Вернуться назад◀️', choosed_lang)))

        # Показываем меню с инлайн-клавиатурой
        bot.send_message(callback.message.chat.id, translate_to_user_language('Твое меню-функций:', choosed_lang),
                         reply_markup=bot_func)

    elif callback.data == 'no':
        bot.send_sticker(callback.message.chat.id, id_sticker_sad)

    # Обработка кнопок-тем в немецком
    open_information_or_worksheet(callback, version, names_themes_standart, names_sheets_standart,
                                  names_themes_vip, names_sheets_vip, section=section)
    try:

        make_lvl_key(callback, choosed_lang, level)

        send_random_game_words(callback, choosed_lang)

        send_first_test_task(callback)

        send_test(callback, choosed_lang, username)
    except AttributeError:
        pass


# Запускаем бота
bot.polling()