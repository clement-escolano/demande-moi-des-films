import csv
from User import User
from random import randint


class Recommendation:

    def __init__(self):

        # Importe la liste des films
        # Dans la variable 'movies_list' se trouve la liste des identifiants des films
        # Dans la variable 'movies' se trouve la correspondance entre l'identifiant d'un film et son titre
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

        # Importe la liste des notations
        # Dans le tableau 'ratings' se trouve un objet avec un attribut 'movie' contenant l'identifiant du film, un
        # attribut 'user' avec l'identifiant de l'utilisateur et un attribut 'isAppreciated' pour savoir si oui ou non
        # l'utilisateur aime le film
        self.ratings = []
        with open('./ml-latest-small/ratings-popular.csv', 'rt', encoding="utf-8") as ratingsFile:
            ratings = csv.reader(ratingsFile, delimiter=',')
            is_first = True
            for rating in ratings:
                if is_first:
                    is_first = False
                    continue
                self.ratings.append({'movie': int(rating[1]), 'user': int(rating[0]), 'isAppreciated': bool(rating[2])})

        # Les utilisateurs du fichier 'ratings.csv' sont stockés dans 'test_users'
        self.test_users = {}
        # Les utilisateurs du chatbot facebook seront stockés dans 'users'
        self.users = {}

        # Lance le traitement des notations
        self.process_ratings_to_users()

    # Traite les notations
    # Crée un utilisateur de test pour chaque utilisateur dans le fichier
    # Puis lui attribue ses films aimés et détestés
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating['user'])
            if rating['isAppreciated']:
                user.good_ratings.append(rating['movie'])
            else:
                user.bad_ratings.append(rating['movie'])
            self.movies_list.append(rating['movie'])

    # Enregistre un utilisateur de test s'il n'existe pas déjà et le retourne
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Enregistre un utilisateur s'il n'existe pas déjà et le retourne
    def register_user(self, sender):
        if sender not in self.users.keys():
            self.users[sender] = User(sender)
        return self.users[sender]

    # Retour les films aimés par un utilisateur
    def get_movies_from_user(self, user):
        movies_list = []
        good_movies = user.good_ratings
        for movie_number in good_movies:
            movies_list.append(self.movies[movie_number])
        return movies_list

    # Affiche la recommandation pour l'utilisateur
    def make_recommendation(self, user):
        return "Vous n'avez pas de recommandation pour le moment.", None

    # Pose une question à l'utilisateur
    def ask_question(self, user):
        return "", None

    # Calcule la similarité entre 2 utilisateurs
    @staticmethod
    def get_similarity(user_a, user_b):
        return 0

    # Calcule la similarité entre un utilisateur et tous les utilisateurs de tests
    def compute_all_similarities(self, user):
        return []
