import telebot
from TelegramBotAPI import types
from telebot import types

bot = telebot.TeleBot('5593220196:AAG0qw4_B_ALDwMv2iWG0AW_pCRvn10CJE0')

number_players = ""
theme = ""
time_out = ""
amount_questions = ""

# init()
    #Map init
        #код комнаты : 1 игрок - админ; остальные игроки

    # API()


def is_free_server():
    return True


def get_next_free_number_of_room():
    pass


def init_session(id, num):
    pass


@bot.message_handler(commands=['start', 'help'])
def start(message, res=False):
    mes = 'Добро пожаловать в мир викторин!\n\n' \
          'Ты можешь стать как создателем игры, так и принять участие уже в существующей партии:\n ' \
          '\n1. Для того, чтобы организовать игру - нажми \'Создать игру\'' \
          '\n2. Если у тебя уже есть код комнаты - нажми \'Войти в игру\'' \
          '\n3. Если у тебя уже есть игра, то для создания новой тебе нужно снчала завершить старую'

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_create = types.KeyboardButton(text='Создать')
    key_open = types.KeyboardButton(text='Войти')
    key_close = types.KeyboardButton(text='Завершить')

    markup.add(key_create, key_open, key_close)
    bot.send_message(message.chat.id, mes, reply_markup=markup)


@bot.message_handler(content_types=['text'])
def dispatcher_of_actions(message):
    if message.text == 'Создать':
        create_game(message)
    if message.text == 'Войти':
        enter_game(message)
    if message.text == 'Завершить':
        close_game(message)


@bot.message_handler(commands=["createGame"])
def create_game(message, res=False):
    global globalCounterOfRooms
    if not is_free_server():
        mes = 'К сожелению, сервер перегружен.\n' \
              'Мест для игры нет!\n' \
              'Зайди чуть позже)'
        bot.send_message(message.chat.id, mes)
    else:
        # num = get_next_free_number_of_room()
        num = 1234
        bot.send_message(message.chat.id, "Твой код команты #" + str(
            num) + "\n\nТеперь можешь поделиться кодом со своими друзьями и начинать квиз. ")
        # success = init_session(message.chat.id, num)
        success = True
        if not success:
            mes = '404 ERROR.\n' \
                  'Зайди чуть позже)'
            bot.send_message(message.chat.id, mes)
        else:
            configure_game(message)


@bot.message_handler(commands=["enterGame"])
def enter_game(message, res=False):
    bot.send_message(message.chat.id, "Напиши код комнаты (номер начинается с #)")


@bot.message_handler(commands=["closeGame"])
def close_game(message, res=False):
    bot.send_message(message.chat.id, "Выход... Пока!")


def configure_game(message):
    bot.send_message(message.chat.id, "Начнем конфигурацию...")
    choose_number_players(message)


@bot.callback_query_handler(func=lambda call: True)
def callback_configure(call):
    global number_players
    global theme
    global time_out
    global amount_questions

    if (call.data == '1' or '2' or '3' or '4') and (number_players == ""):
        number_players = call.data
        choose_theme(call.message)

    elif (call.data == 'Математика' or 'Английский' or 'Java' or 'Общие вопросы') and (theme == ""):
        theme = call.data
        choose_time_out(call.message)

    elif (call.data == '10 сек' or '20 сек') and (time_out == ""):
        time_out = call.data
        choose_amount_questions(call.message)

    elif (call.data == '10' or '20') and (amount_questions == ""):
        amount_questions = call.data
        start_game(call.message)


def choose_number_players(message):
    markup = types.InlineKeyboardMarkup()
    key_one = types.InlineKeyboardButton(text='1', callback_data='1')
    key_two = types.InlineKeyboardButton(text='2', callback_data='2')
    key_three = types.InlineKeyboardButton(text='3', callback_data='3')
    key_four = types.InlineKeyboardButton(text='4', callback_data='4')
    markup.add(key_one, key_two, key_three, key_four)
    bot.send_message(message.chat.id, "Настройка 1/4: Кол-во игроков", reply_markup=markup)


def choose_theme(message):
    markup = types.InlineKeyboardMarkup()
    key_math = types.InlineKeyboardButton(text='Математика', callback_data='Математика')
    key_english = types.InlineKeyboardButton(text='Английский', callback_data='Английский')
    key_java = types.InlineKeyboardButton(text='Java', callback_data='Java')
    key_gen = types.InlineKeyboardButton(text='Общие вопросы', callback_data='Общие вопросы')

    markup.add(key_math, key_english, key_java, key_gen)
    bot.send_message(message.chat.id, "Настройка 2/4: Тема", reply_markup=markup)


def choose_time_out(message):
    markup = types.InlineKeyboardMarkup()
    key_10 = types.InlineKeyboardButton(text='10 сек', callback_data='10 сек')
    key_20 = types.InlineKeyboardButton(text='20 сек', callback_data='20 сек')

    markup.add(key_10, key_20)
    bot.send_message(message.chat.id, "Настройка 3/4: Тайм аут", reply_markup=markup)


def choose_amount_questions(message):
    markup = types.InlineKeyboardMarkup()
    key_10 = types.InlineKeyboardButton(text='10', callback_data='10')
    key_20 = types.InlineKeyboardButton(text='20', callback_data='20')

    markup.add(key_10, key_20)
    bot.send_message(message.chat.id, "Настройка 4/4: Кол-во вопросов", reply_markup=markup)


def start_game(message):
    print("ID: " + str(message.chat.id) + "\n")
    print("Кол-во игроков: " + number_players + "\nТема: " + theme + "\nВремя ожидания ответа на вопрос: " + time_out + "\nКол-во вопросов: " + amount_questions)


bot.polling(none_stop=True, interval=0)
