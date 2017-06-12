from time import time
from math import sqrt

question_delay = 5 * 60


class User:

    def __init__(self, sender_id):
        self.id = sender_id
        self.good_ratings = []
        self.bad_ratings = []
        self.neutral_ratings = []
        self.latest_movie_asked = None
        self.questions_before_recommendation = None
        self.question_asked_time = None

    def answer_yes(self):
        self.good_ratings.append(self.latest_movie_asked)
        self.latest_movie_asked = None
        self.questions_before_recommendation -= 1

    def answer_no(self):
        self.bad_ratings.append(self.latest_movie_asked)
        self.latest_movie_asked = None
        self.questions_before_recommendation -= 1

    def answer_neutral(self):
        self.neutral_ratings.append(self.latest_movie_asked)
        self.latest_movie_asked = None

    def set_question(self, movie_number):
        self.latest_movie_asked = movie_number
        if self.questions_before_recommendation is None or self.questions_before_recommendation <= 0:
            self.questions_before_recommendation = 10
        self.question_asked_time = int(time())

    def answer_question(self, message):
        clean_message = message.lower().strip()
        if self.latest_movie_asked and int(time()) - self.question_asked_time < question_delay:
            if "oui" in clean_message:
                self.answer_yes()
                return True
            elif "non" in clean_message:
                self.answer_no()
                return True
            else:
                self.answer_neutral()
                return True
        self.latest_movie_asked = None
        return False

    def should_make_recommendation(self):
        return self.questions_before_recommendation <= 0

    def get_norm(self):
        norm = 1 + (len(self.good_ratings) + len(self.bad_ratings)) ** 2
        return sqrt(norm)

    @staticmethod
    def get_similarity(user_a, user_b):
        score = 0
        for good_rating in user_a.good_ratings:
            if good_rating in user_b.good_ratings:
                score += 1
        for bad_rating in user_a.bad_ratings:
            if bad_rating in user_b.bad_ratings:
                score -= 1
        return score / (user_a.get_norm() * user_b.get_norm())
