import telebot
from TelegramBotAPI import types
from telebot import types

from Session import Session

bot = telebot.TeleBot('5593220196:AAG0qw4_B_ALDwMv2iWG0AW_pCRvn10CJE0')

sessions = list()
limit_of_sessions = 100
last_generated_number = 0

# GENERAL
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
    key_start_session = types.KeyboardButton(text='Начать игру')

    markup.add(key_create, key_open, key_close, key_start_session)
    bot.send_message(message.chat.id, mes, reply_markup=markup)

@bot.message_handler(commands=["beginGame"])
def start_game(message):
    currentSession = None
    for i in sessions:
        if i.admin_id == message.chat.id:
            currentSession = i
            break
    if currentSession == None:
        return

    for i in currentSession.players:
        mes = bot.send_message(i, "Игра начинается!")
        bot.register_next_step_handler(mes, next_question, i, currentSession, False)


def timeout(currentSession):
    waiting_list = currentSession.get_waiting_list()
    for player_id in currentSession.players:
        if currentSession.get_next_question(player_id) >= currentSession.number_of_questions:
            continue

        if player_id in waiting_list:
            pass
        else:
            continue

        currentSession.set_answer(player_id , currentSession.get_next_question(player_id), "")
    
        message = bot.send_message(player_id, "Время истекло, переходим к следующему вопросу")

        battle = currentSession.questions[currentSession.get_next_question(player_id)]
    
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        answ1 = types.KeyboardButton(text=battle.correct_answer)
        answ2 = types.KeyboardButton(text=battle.incorrect_answers[0])
        answ3 = types.KeyboardButton(text=battle.incorrect_answers[1])
        answ4 = types.KeyboardButton(text=battle.incorrect_answers[2])
    
        markup.add(answ1, answ2, answ3, answ4)
    
        bot.send_message(player_id, battle.question, reply_markup=markup)
        bot.register_next_step_handler(message, next_question, player_id, currentSession, True)

def next_question(message, player_id, currentSession, flag):

    if flag:
        currentSession.set_answer(player_id , currentSession.get_next_question(player_id), message.text)
        message = bot.send_message(player_id, "Ваш ответ принят, ждем остальных")
        while currentSession.get_n_waiting_to_answer > 0:
            pass
    
    
    if currentSession.get_next_question(player_id) >= currentSession.number_of_questions:
        bot.send_message(player_id, "Your score: " + str(currentSession.get_results(player_id)) + "/" + str(currentSession.number_of_questions))
        return

    battle = currentSession.questions[currentSession.get_next_question(player_id)]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    answ1 = types.KeyboardButton(text=battle.correct_answer)
    answ2 = types.KeyboardButton(text=battle.incorrect_answers[0])
    answ3 = types.KeyboardButton(text=battle.incorrect_answers[1])
    answ4 = types.KeyboardButton(text=battle.incorrect_answers[2])

    markup.add(answ1, answ2, answ3, answ4)

    bot.send_message(player_id, battle.question, reply_markup=markup)
    bot.register_next_step_handler(message, next_question, player_id, currentSession, True)

@bot.message_handler(content_types=['text'])
def dispatcher_of_actions(message):
    if message.text == 'Создать':
        create_game(message)
    if message.text == 'Войти':
        enter_game(message)
    if message.text == 'Завершить':
        close_game(message)
    if message.text == 'Начать игру':
        start_game(message)

# ADMIN
def is_free_server():
    return not len(sessions) >= limit_of_sessions
def get_next_free_number_of_room():
    all_n = []
    for i in sessions:
        all_n.append(i.room_id)

    for i in range(1, limit_of_sessions + 1):
        if not all_n.__contains__(i):
            return i

@bot.message_handler(commands=["createGame"])
def create_game(message, res=False):
    global sessions

    if not is_free_server():
        mes = 'К сожелению, сервер перегружен.\n' \
              'Мест для игры нет!\n' \
              'Зайди чуть позже)'
        bot.send_message(message.chat.id, mes)

    else:
        num = get_next_free_number_of_room()
        sessions.append(Session(message.chat.id, num, ))
        bot.send_message(message.chat.id, "Твой код команты #" + str(num) +
                         "\n\nТеперь можешь поделиться кодом со своими друзьями и начинать квиз. ")
        configure_session(message)

def configure_session(message):
    bot.send_message(message.chat.id, "Начнем конфигурацию...")
    choose_number_players(message)

@bot.callback_query_handler(func=lambda call: True)
def callback_configure(call):
    currentSession = None

    for i in sessions:
        if i.admin_id == call.message.chat.id:
            currentSession = i
            break

    if ((call.data == '1') or (call.data == '2') or (call.data == '3') or (call.data == '4')) and (currentSession.number_of_players == 0):
        currentSession.number_of_players = call.data
        call.data = ''
        choose_theme(call.message)

    elif ((call.data == 'arts_and_literature') or (call.data == 'film_and_tv') or (call.data == 'food_and_drink') or (call.data == 'general_knowledge')) and (currentSession.theme == ""):
        currentSession.theme = call.data
        call.data = ''
        choose_amount_questions(call.message)

    elif ((call.data == '10') or (call.data == '20')) and (currentSession.number_of_questions == 0):
        currentSession.number_of_questions = int(call.data)
        currentSession.init_questions()
        call.data = ''
        start(call.message)

def choose_number_players(message):
    markup = types.InlineKeyboardMarkup()
    key_one = types.InlineKeyboardButton(text='1', callback_data='1')
    key_two = types.InlineKeyboardButton(text='2', callback_data='2')
    key_three = types.InlineKeyboardButton(text='3', callback_data='3')
    key_four = types.InlineKeyboardButton(text='4', callback_data='4')
    markup.add(key_one, key_two, key_three, key_four)
    bot.send_message(message.chat.id, "Настройка 1/3: Кол-во игроков", reply_markup=markup)

def choose_theme(message):
    markup = types.InlineKeyboardMarkup()
    key_math = types.InlineKeyboardButton(text='Arts & Literature', callback_data='arts_and_literature')
    key_english = types.InlineKeyboardButton(text='Film & TV', callback_data='film_and_tv')
    key_java = types.InlineKeyboardButton(text='Food & Drink', callback_data='food_and_drink')
    key_gen = types.InlineKeyboardButton(text='General Knowledge', callback_data='general_knowledge')

    markup.add(key_math, key_english, key_java, key_gen)
    bot.send_message(message.chat.id, "Настройка 2/3: Тема", reply_markup=markup)

def choose_amount_questions(message):
    markup = types.InlineKeyboardMarkup()
    key_10 = types.InlineKeyboardButton(text='10', callback_data='10')
    key_20 = types.InlineKeyboardButton(text='20', callback_data='20')

    markup.add(key_10, key_20)
    bot.send_message(message.chat.id, "Настройка 3/3: Кол-во вопросов", reply_markup=markup)

# ADMIN AND PLAYER
@bot.message_handler(commands=["enterGame"])
def enter_game(message, res=False):
    bot.send_message(message.chat.id, "Напиши код комнаты (номер начинается с #)")
    bot.register_next_step_handler(message, read_number_of_room)

def read_number_of_room(message):
    number = message.text
    # check
    currentSession = None
    for i in sessions:
        if str(i.room_id) == number:
            currentSession = i
            break

    currentSession.set_new_player(message.chat.id)

@bot.message_handler(commands=["closeGame"])
def close_game(message, res=False):
    bot.send_message(message.chat.id, "Выход... Пока!")

bot.polling(none_stop=True, interval=0)
