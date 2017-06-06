import csv
from User import User
from random import randint


class Recommendation:

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
    def make_recommendation(user):
        return "Je n'ai pas de recommendation à vous faire. " + str(user.id)

    def ask_question(self, user):
        movie_number = self.movies_list[randint(0, len(self.movies_list))]
        user.latest_movie_asked = movie_number
        if user.questions_before_recommendation is None or user.questions_before_recommendation <= 0:
            user.questions_before_recommendation = 5
        return "Avez-vous aimé : " + self.movies[movie_number]
