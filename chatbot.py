# coding: utf-8

import csv
from random import randint

from User import User


class Bot(object):

    def __init__(self):
        self.movies_list = []
        self.movies = dict()
        with open('./ml-latest-small/movies.csv', 'rt', encoding="utf-8") as moviesFile:
            movies = csv.reader(moviesFile, delimiter=',')
            is_first = True
            for movie in movies:
                if is_first:
                    is_first = False
                    continue
                self.movies[movie[0]] = movie[1]
                self.movies_list.append(movie[0])

        self.ratings = []
        with open('./ml-latest-small/ratings.csv', 'rt', encoding="utf-8") as ratingsFile:
            ratings = csv.reader(ratingsFile, delimiter=',')
            is_first = True
            for rating in ratings:
                if is_first:
                    is_first = False
                    continue
                self.ratings.append({'movie': rating[1], 'user': rating[0], 'score': rating[2]})

        self.users = {}

    def register_user(self, sender):
        if sender not in self.users.keys():
            self.users[sender] = User(sender)
        return self.users[sender]

    @staticmethod
    def answer_question(user, message):
        clean_message = message.lower().strip()
        if user.latest_movie_asked:
            if "oui" in clean_message:
                user.answer_yes()
                return True
            elif "non" in clean_message:
                user.answer_no()
                return True
            else:
                user.latest_movie_asked = None
        return False

    @staticmethod
    def should_make_recommendation(user):
        return user.questions_before_recommendation <= 0

    @staticmethod
    def make_recommendation(user):
        return "bla: " + str(user.id)

    def ask_question(self, user):
        movie_number = self.movies_list[randint(0, len(self.movies_list))]
        user.latest_movie_asked = movie_number
        return "Avez-vous aimé : " + self.movies[movie_number]

    def respond_to(self, sender, message):
        user = self.register_user(sender)
        if not self.answer_question(user, message):
            user.questions_before_recommendation = 5
            return self.ask_question(user)
        else:
            if self.should_make_recommendation(user):
                return self.make_recommendation(user)
            else:
                return self.ask_question(user)
