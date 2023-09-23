"""В этом файле будут храниться токены, либо айди, чтобы избежать потери токена.
   Также словари с кнопками, со словами для игры 'Как на Drutsch?' и тд."""

from os import listdir

# Токен от бота.
telegram_bot_token = ''

# айди GIFа с названием бота.
animation_id = 'CgACAgIAAxkBAAIGcmS-TozQEp5xd5v_8BkjeLSZoNYDAALQLAACrGXxSc83ri4Ej57eLwQ'

# айди грустного стикера
id_sticker_sad = 'CAACAgIAAxkBAAIJV2TDqNwc-HUJizZKpOFuY9DsdexuAAIOAAPANk8TI1cURIdu1mUvBA'

bd_name = 'serverus.db'

# Словарь возможных языков для выбора
AVAILABLE_LANGUAGES = {
    'ru': 'Русский🇷🇺',
    'uk': 'Українська🇺🇦',
    'en': 'English🇺🇸'
}

# Словарь для меню-клавиатуры
AVAILABLE_BUTTONS = {
    'tokens': 'Токены🤑',
    'version': 'Версия😎',
    'menu': 'Меню📋',
    'buy_ver': 'Купить версию🌕'
}

# Словарь для меню-клавиатуры 2
BUTTONS_TRANSLATIONS = {
    'ru': {
        'tokens': 'Токены🤑',
        'version': 'Версия😎',
        'menu': 'Меню📋',
        'buy_ver': 'Купить версию🌕'
    },
    'uk': {
        'tokens': 'Токени🤑',
        'version': 'Версія😎',
        'menu': 'Меню📋',
        'buy_ver': 'Купити версію🌕'
    },
    'en': {
        'tokens': 'Tokens🤑',
        'version': 'Version😎',
        'menu': 'Menu📋',
        'buy_ver': 'Buy version🌕'
    }
}

# Делаем меню функций бота
list_bot_function = {'deutsch': 'Как на Deutsch?',
                     'information': 'Information_themes🤓',
                     'worksheets': 'Рабочие листы📄',
                     'test': 'Pass the test🧑‍💻'}

# Делаем меню функций бота 2
list_bot_function2 = {
    'ru': {
        'deutsch': 'Как на Deutsch🇩🇪?',
        'information': 'Информация на темы🤓',
        'worksheets': 'Рабочие листы📄',
        'test': 'Пройти тест🧑‍💻'
    },
    'uk': {
        'deutsch': 'Як на Deutsch?🇩🇪',
        'information': 'Інформація про теми🤓',
        'worksheets': 'Робочі аркуші📄',
        'test': 'Пройти тест🧑‍💻'
    },
    'en': {
        'deutsch': 'How on Deutsch?🇩🇪',
        'information': 'Information on topics🤓',
        'worksheets': 'Working sheets📄',
        'test': 'Pass the test🧑‍💻'
    }
}

# Текст для обработки команды /help
list_commands = """<b>Список команд:</b>
/help - Посмотреть все команды пользователя
/token - Посмотреть количество токенов
/version - Посмотреть версию
/start - Старт бота"""

# Текст для приветствия пользователя
great = "<b>Привет!</b>\n""Добро пожаловать в <b>German Helper</b> - бот-помощник по немецкому языку! 🇩🇪🤖"


# Список эмодзи
emojis = ["😀", "☺️", "😗", "🤓", "😏", "😮‍💨", "👍🏻", "👨🏼‍🦲", "🧙‍♂️", "🐱", "🐶", "🙉", "🐸", "🐽", "🐻‍❄️",
          "🐼", "🐍", "🦀", "🦧", "🐁", "🪶", "🐑", "🌚", "🌕", "🍋", "🧀", "🥞", "🌽", "🌶", "🍓", "🥝", "🥥", "🏀", "⚽",
          "🥎", "🏸", "🔴", "🟠", "🟡", "🟢", "🔵", "🟣", "⚫️", "⚪️", "🟤", "♥️"]


# Пути к файлам с информацией о темах для стандартной и VIP версии
names_themes_standart = 'German_Helper/standart_version/Information_themes/'
names_themes_vip = 'German_Helper/vip version/themes_information'


# Пути к файлам с рабочими листами для стандартной и VIP версии
names_sheets_vip = 'German_Helper/vip version/sheets_work'
names_sheets_standart = 'German_Helper/standart_version/work_sheets'


# Переменные для корректного и неправильного ответа в игре
correct_answer = f'✅ Молодец, ты ответил правильно!\n'
false_answer = '❌К сожалению, это не правильный ответ, правильно будет: '


# Текст для задания в игре
say_task = f'Как будет это слово на немецком: '

# Правила игры
regel_game = f'''\t <b>Правила игры</b>
В начале ты выбераешь три уровня:
A1, A2, B1.
Взависимости от сложности уровня будет отличаться количество токенов:
A1-1токен, A2-2токена,  B1-3 токена.
Чтобы остановить игру напиши /stop_game.
Удачи!😀'''

# Правила теста
regel_test = '''<b> Этот тест поможет тебе узнать,
насколько хорошо ты знаешь немецкий.😀</b>
Всего будет '''

# Уровни результата теста
level_a0 = '''<b>🌟Поздровляю!🌟</b>
По моим расчетам, у тебя <b>А0</b>.
Ты еще не сильно знаешь грамматику, и 
не сильно понимаешь задания в этом тесте.
Для новичка это не плохой результат!
Трудись и учи грамматику и слова и тогда все получиться!
'''

level_a1 = '''<b>🌟Поздровляю!🌟</b>
По моим расчетам, у тебя <b>А1</b>.
Ты еще не сильно знаешь грамматику,
но ты уже можешь понимать простой текст.
Для новичка это отличный результат!
Трудись и все получиться!'''

level_a2 = '''<b>🌟Поздровляю!🌟</b>
По моим расчетам, у тебя <b>А2</b>.
Ты уже можешь понимать небольшой текст,
знаешь неплохое количество слов,
и уже немного знаешь грамматику немецкого.
Трудись и все получиться!'''

level_b1 = '''<b>🌟Поздровляю!🌟</b>
По моим расчетам, у тебя <b>B1</b>.
Ты отлично сдал этот тест.
У тебя отличный словарный запас, 
ты хорошо знаешь грамматику немецкого,
и разбираешься в заданиях.
Трудись и все получиться!'''


# Случайные похвалы и утешения
random_great_words = ['Молодець!', 'Отлично!', 'Правильно!', 'Неплохо!', 'Умница!', 'Браво!', 'Замечательно!',
                      'Фантастика!', 'Прекрасно!', 'Восхитительно!']
random_false_words = ['Не правильно!', 'Вы ошиблись..', 'Не точно.']


# Сообщение о покупке VIP версии
buy_vip = '''<b>🌟Поздровляю!🌟</b>
Ты купил <b>"vip"</b> версию.
Теперь у тебя есть больше выбора.
Вместо 10 тем, у тебя теперь будет 20.
Соответственно, у тебя будет больше выбора,
и ты еще эфективнее будешь учить немецкий.
<b>Удачи!</b>'''