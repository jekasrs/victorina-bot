import requests
import json

from Question import Question
from threading import Timer


class Session:
    def __init__(self, new_admin_id, new_room_id):
        self.set_admin_id(new_admin_id)  # id чата создателя
        self.set_room_id(new_room_id)  # номер комнаты

        self.number_of_players = 0  # кол-во игроков
        self.number_of_questions = 0  # кол-во вопросов
        self.n_waiting_to_answer = 0
        self.set_theme("")  # время ответа на вопрос

        self.timer

        self.waiting_list = list()
        self.players = list()
        self.questions = list()
        self.answers = dict()
        self.players.append(new_admin_id)
        self.answers[str(new_admin_id)] = list()

    def get_waiting_list(self):
        return self.waiting_list
    
    def set_timer(self, timeout):
        self.timer = Timer(10.0, timeout(self) )
        self.timer.start()

    def set_new_player(self, player_id):
        if len(self.players) == self.number_of_players:
            return
        self.players.append(player_id)
        self.answers[str(player_id)] = list()
        print(len(list()))
        print(len(self.answers[str(player_id)]))

    def get_admin_id(self):
        return self.admin_id

    def set_admin_id(self, new_admin_id):
        self.admin_id = new_admin_id

    def get_room_id(self):
        return self.room_id

    def set_room_id(self, new_room_id):
        self.room_id = new_room_id

    def get_number_of_players(self):
        return self.number_of_players

    def set_number_of_players(self, new_number_of_players):
        if new_number_of_players < 1:
            return
        self.n_waiting_to_answer = new_number_of_players
        self.number_of_players = new_number_of_players
        
    def get_n_waiting_to_answer(self):
        return self.n_waiting_to_answer
    
    def get_number_of_questions(self):
        return self.number_of_players

    def set_number_of_questions(self, new_number_of_questions):
        if new_number_of_questions < 1:
            return
        self.number_of_questions = new_number_of_questions

    def get_theme(self):
        return self.theme

    def set_theme(self, new_theme):
        self.theme = new_theme

    def init_questions(self):
        print('https://the-trivia-api.com/api/questions?categories=' + self.theme + '&limit=' + str(
            self.number_of_questions) + '\n\n')

        req = requests.get('https://the-trivia-api.com/api/questions?categories=' + self.theme + '&limit=' + str(
            self.number_of_questions))

        if req.status_code > 299:
            print("no access")
        else:
            print("success")

        questions_arr = json.loads(req.text)
        print(questions_arr)
        for i in questions_arr:
            q = Question(i['question'], i['correctAnswer'], i['incorrectAnswers'])
            self.questions.append(q)

    def set_answer(self, player_id, question_id, answer):
        self.waiting_list.remove(player_id)
        self.timer.cancel()
        self.n_waiting_to_answer = self.n_waiting_to_answer  - 1
        if self.questions[question_id].correct_answer == answer:
            self.answers[str(player_id)].append(1)
        else:
            self.answers[str(player_id)].append(0)

    def get_results(self, player_id):
        print(self.answers[str(player_id)])
        return sum(self.answers[str(player_id)])

    def get_next_question(self, player_id):
        self.waiting_list.append(player_id)
        self.n_waiting_to_answer = self.number_of_players
        return len(self.answers[str(player_id)])

