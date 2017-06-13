import csv
from User import User
from random import randint


class Recommendation:

    def __init__(self):
        self.movies_list = []
        self.movies = dict()
        with open('./ml-latest-small/movies-popular.csv', 'rt', encoding="utf-8") as moviesFile:
            movies = csv.reader(moviesFile, delimiter=',')
            is_first = True
            for movie in movies:
                if is_first:
                    is_first = False
                    continue
                self.movies[int(movie[0])] = movie[1]

        self.ratings = []
        with open('./ml-latest-small/ratings-popular.csv', 'rt', encoding="utf-8") as ratingsFile:
            ratings = csv.reader(ratingsFile, delimiter=',')
            is_first = True
            for rating in ratings:
                if is_first:
                    is_first = False
                    continue
                self.ratings.append({'movie': int(rating[1]), 'user': int(rating[0]), 'isAppreciated': bool(rating[2])})

        self.test_users = {}
        self.users = {}
        self.process_ratings_to_users()

    def process_ratings_to_users(self):
        for rating in self.ratings:
            if rating['user'] not in self.test_users.keys():
                self.test_users[rating['user']] = User(rating['user'])
            user = self.test_users[rating['user']]
            if rating['isAppreciated']:
                user.good_ratings.append(rating['movie'])
            else:
                user.bad_ratings.append(rating['movie'])
            self.movies_list.append(rating['movie'])

    def register_user(self, sender):
        if sender not in self.users.keys():
            self.users[sender] = User(sender)
        return self.users[sender]

    def make_recommendation(self, user):
        similarities = self.compute_all_similarities(user)
        similarities.sort()
        similarities.reverse()
        best_match = similarities[0][1]
        best_match_user = self.test_users[best_match]
        recommendations = self.get_movies_from_user(best_match_user)[0:3]
        return ("Vos recommandations : " + ", ".join(recommendations)), None

    def ask_question(self, user):
        movie_number = self.movies_list[randint(0, len(self.movies_list))]
        user.set_question(movie_number)
        return ("Avez-vous aimé : " + self.movies[movie_number]), ["Oui", "Non", "Pas vu"]

    def compute_all_similarities(self, user):
        similarities = []
        for other_user in self.test_users.values():
            similarities.append((User.get_similarity(user, other_user), other_user.id))
        return similarities

    def get_movies_from_user(self, user):
        movies_list = []
        good_movies = user.good_ratings
        for movie_number in good_movies:
            movies_list.append(self.movies[movie_number])
        return movies_list
