class Question:

    def __init__(self, question, correct_answer, incorrect_answer):
        self.question = question
        self.correct_answer = correct_answer
        self.incorrect_answers = incorrect_answer

    def get_question(self):
        return self.question

    def get_correct_answer(self):
        return self.correct_answer

    def get_incorrect_answers(self):
        return self.incorrect_answers
