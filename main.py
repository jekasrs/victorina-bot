from random import shuffle

import telebot
from TelegramBotAPI import types
from telebot import types

from Session import Session

bot = telebot.TeleBot('5593220196:AAG0qw4_B_ALDwMv2iWG0AW_pCRvn10CJE0')

sessions = list()
limit_of_sessions = 100

# Если не найдена, то возвращается None
def findSessionById(message):
    global sessions
    currentSession = None
    for i in sessions:
        if message.chat.id in i.players:
            currentSession = i
            break
    return currentSession

def isAdmin(massage, currentSession):
    return massage.chat.id == currentSession.get_admin_id()

# можно ли создать еще команту
def is_free_server():
    global sessions
    global limit_of_sessions
    return not len(sessions) >= limit_of_sessions

# получение номера команты для админа
def get_next_free_number_of_room():
    global sessions
    global limit_of_sessions
    all_n = []
    for i in sessions:
        all_n.append(i.room_id)

    for i in range(1, limit_of_sessions + 1):
        if not all_n.__contains__(i):
            return i

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

    currentSesion = findSessionById(message)

    # не игрок еще
    if currentSesion is None:
        markup.add(key_create, key_open)

    # уже игрок
    else:
        # меню для админа
        if isAdmin(message, currentSesion):
            markup.add(key_close, key_start_session)

        # меню для игрока
        else:
            markup.add(key_open, key_close)

    bot.send_message(message.chat.id, mes, reply_markup=markup)

# Запуск игры: старт сессии
@bot.message_handler(commands=["beginGame"])
def start_game(message):
    currentSession = findSessionById(message)
    if currentSession is None:
        return

    # как посмотреть, что уже есть ответы в сессии
    if currentSession.is_finished:
        for p in currentSession.players:
            currentSession.answers[str(p)] = list()
        currentSession.is_finished = False
        currentSession.init_questions()

    currentSession.how_many_finished = len(currentSession.players)
    for i in currentSession.players:
        mes = bot.send_message(i, "Игра начинается!")
        next_question(mes, i, currentSession, False)

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
        
# создание игры, бронирование номера и запуск процесса конфигурации
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
        sessions.append(Session(message.chat.id, num))
        bot.send_message(message.chat.id, "Твой код команты #" + str(num) +
                         "\n\nТеперь можешь поделиться кодом со своими друзьями и начинать квиз. ")
        configure_session(message)

# вход в команту
@bot.message_handler(commands=["enterGame"])
def enter_game(message, res=False):
    bot.send_message(message.chat.id, "Напиши код комнаты")
    bot.register_next_step_handler(message, read_number_of_room)

# выход из команты
@bot.message_handler(commands=["closeGame"])
def close_game(message, res=False):
    currentSession = findSessionById(message)
    if (currentSession is None):
        bot.send_message(message.chat.id, "Вы и так не в комнате, чтоыб выйти из неё.")
        return

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    key_create = types.KeyboardButton(text='Создать')
    key_open = types.KeyboardButton(text='Войти')
    markup.add(key_create, key_open)

    if isAdmin(message, currentSession):
        for p in currentSession.players:
            bot.send_message(p, "Создатель комнаты завершил игру!", reply_markup=markup)
        sessions.remove(currentSession)
    else:
        currentSession.players.remove(message.chat.id)
        bot.send_message(message.chat.id, "Выход из команты. Пока...", reply_markup=markup)

# оповещение о ночале конфигурации
def configure_session(message):
    bot.send_message(message.chat.id, "Начнем конфигурацию...", reply_markup=telebot.types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, "Настройка 1/3: Кол-во игроков (от 1 до 3)")
    bot.register_next_step_handler(message, read_number_of_players)

def read_number_of_players(message):
    if str(message.text) == str('1') or str(message.text) == str('2') or str(message.text) == str('3'):
        currentSession = findSessionById(message)
        currentSession.number_of_players = int(message.text)
        bot.send_message(message.chat.id, "Настройка 2/3: Тема")
        bot.register_next_step_handler(message, read_theme)

    else:
        bot.send_message(message.chat.id, "Вы должны ввести число от 1 до 3 \n")
        configure_session(message)
        return

def read_theme(message):
    currentSession = findSessionById(message)
    currentSession.set_theme(message.text)
    bot.send_message(message.chat.id, "Настройка 3/3: Кол-во вопросов (10 или 20)")
    bot.register_next_step_handler(message, read_number_of_question)

def read_number_of_question(message):
    if str(message.text) == str('10') or str(message.text) == str('20'):
        currentSession = findSessionById(message)
        currentSession.number_of_questions = int(message.text)
        currentSession.init_questions()
        start(message)

    else:
        bot.send_message(message.chat.id, "Настройка 3/3: Кол-во вопросов (10 или 20)")
        bot.register_next_step_handler(message, read_number_of_question)
        return

# попытка добавить игрока в команту
def read_number_of_room(message):
    if not message.text.isdigit():
        bot.send_message(message.chat.id, "Номер комнаты - число\nНажмите кнопку Войти или Создать")
        return
    number = message.text
    currentSession = None
    for i in sessions:
        if str(i.room_id) == number:
            currentSession = i
            break
    if currentSession is None:
        bot.send_message(message.chat.id, "Такой комнаты не существует. Уточните номер у админа.\nНажмите кнопку Войти или Создать")
        return
    if len(currentSession.players) == currentSession.number_of_players:
        bot.send_message(message.chat.id, "Комната уже полностью заполненена. Создайте новую или выбирите другую.\nНажмите кнопку Войти или Создать")
        return
    currentSession.set_new_player(message.chat.id)
    bot.send_message(message.chat.id, "Вы подключились к комнате #" + str(currentSession.room_id) + "\nОжидайте начала игры. ")

# следующий ход
def next_question(message, player_id, currentSession, flag):
    if flag:
        currentSession.set_answer(player_id, currentSession.get_next_question(player_id), message.text)

    if currentSession.get_next_question(player_id) >= currentSession.number_of_questions:
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        key_close = types.KeyboardButton(text='Завершить')
        key_start_session = types.KeyboardButton(text='Начать игру')
        currentSession.is_finished = True

        # меню для админа
        if isAdmin(message, currentSession):
            markup.add(key_close, key_start_session)

        # меню для игрока
        else:
            markup.add(key_close)

        currentSession.how_many_finished = currentSession.how_many_finished-1
        bot.send_message(player_id, "Ждём остальных...", reply_markup=markup)

        if currentSession.how_many_finished == 0:
            leaderBoard = str("Рейтинг игроков:\n")
            for playerid in currentSession.get_players():
                UsrInfo = bot.get_chat_member(playerid, playerid).user
                if currentSession.get_results(playerid)/currentSession.number_of_questions < 0.2 :
                    leaderBoard = leaderBoard + "\n💩 @" + str(UsrInfo.username) + " : " + str(currentSession.get_results(playerid)) + "/" + str(currentSession.number_of_questions)

                elif currentSession.get_results(playerid)/currentSession.number_of_questions < 0.5 :
                    leaderBoard = leaderBoard + "\n🧐️ @" + str(UsrInfo.username) + " : " + str(currentSession.get_results(playerid)) + "/" + str(currentSession.number_of_questions)

                elif currentSession.get_results(playerid)/currentSession.number_of_questions == 0.5 :
                    leaderBoard = leaderBoard + "️️\n⚖ @" + str(UsrInfo.username) + " : " + str(currentSession.get_results(playerid)) + "/" + str(currentSession.number_of_questions)

                else:
                    leaderBoard = leaderBoard + "️️\n🥇 @" + str(UsrInfo.username) + " : " + str(currentSession.get_results(playerid)) + "/" + str(currentSession.number_of_questions)

            for playerid in currentSession.get_players():
                bot.send_message(playerid, leaderBoard, reply_markup=markup)

        return

    battle = currentSession.questions[currentSession.get_next_question(player_id)]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)

    possible_answers = list()
    possible_answers.append(battle.correct_answer)
    possible_answers.append(battle.incorrect_answers[0])
    possible_answers.append(battle.incorrect_answers[1])
    possible_answers.append(battle.incorrect_answers[2])
    shuffle(possible_answers)
    answ1 = types.KeyboardButton(text=possible_answers[0])
    answ2 = types.KeyboardButton(text=possible_answers[1])
    answ3 = types.KeyboardButton(text=possible_answers[2])
    answ4 = types.KeyboardButton(text=possible_answers[3])

    markup.add(answ1, answ2, answ3, answ4)
    bot.send_message(player_id, battle.question, reply_markup=markup)
    bot.register_next_step_handler(message, next_question, player_id, currentSession, True)

bot.polling(none_stop=True, interval=0)
