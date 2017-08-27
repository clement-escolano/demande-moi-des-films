# coding: utf-8

# Handle the logic of the chatbot: how to answer questions, what to do with messages and so on.

from random import randint

from app.User import User
from app.movielens import MovieLens
from app.recommendation import Recommendation


class Bot(object):

    def __init__(self):
        self.movielens = MovieLens()
        self.recommendation = Recommendation(self.movielens)
        self.movie_picker = MoviePicker(self.movielens)
        self.users = {}

    def respond_to(self, sender, message):
        user = self.register_user(sender)
        user.process_message(message)

        if user.should_make_recommendation():
            user.reset_remaining_questions_number()
            return self.recommendation.make_recommendation(user)
        else:
            intro = ""
            # If the user speak for the first time, display a welcome message
            if not user.has_been_asked_a_question():
                intro = "Bonjour ! Je vais vous poser des questions puis vous faire une recommandation.\n"

            message = self.ask_question(user)
            return intro + message

    # Register a user if it does not exist and return it
    def register_user(self, sender):
        if sender not in self.users.keys():
            self.users[sender] = User(sender)
        return self.users[sender]

    def ask_question(self, user):
        movie = self.movie_picker.pick_a_movie()
        user.set_pending_question(movie)
        return "Avez-vous aimé : " + movie.title + " ?"


# Take a movie randomly
# However, the more ratings for a movie, the more often it is picked
class MoviePicker:

    def __init__(self, movielens):
        self.movielens = movielens
        self.movie_list = []
        for rating in movielens.simplified_ratings:
            self.movie_list.append(rating.movie)

    def pick_a_movie(self):
        movie_number = self.movie_list[randint(0, len(self.movie_list))]
        return self.movielens.movies[movie_number]
