# coding: utf-8

from app.User import User


class Recommendation:

    def __init__(self, movielens):

        # Importe la liste des films
        # Dans la variable 'movies' se trouve la correspondance entre l'identifiant d'un film et le film
        # Dans la variables 'movies_list' se trouve les films populaires qui sont vus par les utilisateurs
        self.movies = movielens

        # Importe la liste des notations
        # Dans le tableau 'ratings' se trouve un objet avec un attribut 'movie' contenant l'identifiant du film, un
        # attribut 'user' avec l'identifiant de l'utilisateur et un attribut 'is_appreciated' pour savoir si oui ou non
        # l'utilisateur aime le film
        self.ratings = movielens.simplified_ratings

        # Les utilisateurs du fichier 'ratings-popular-simplified.csv' sont stockés dans 'test_users'
        self.test_users = {}

        # Lance le traitement des notations
        self.process_ratings_to_users()

    # Traite les notations
    # Crée un utilisateur de test pour chaque utilisateur dans le fichier
    # Puis lui attribue ses films aimés et détestés
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            if rating.is_appreciated is not None:
                if rating.is_appreciated:
                    user.good_ratings.append(rating)
                else:
                    user.bad_ratings.append(rating)
            elif rating.score is not None:
                user.ratings.append(rating)

    # Enregistre un utilisateur de test s'il n'existe pas déjà et le retourne
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Retourne les films aimés par un utilisateur
    def get_movies_from_user(self, user):
        movies_list = []
        good_movies = user.good_ratings
        for movie in good_movies:
            movies_list.append(movie.title)
        return movies_list

    def get_best_movies_from_users(self, users):
        # Dictionnaire comptant le nombre d'occurences de chaque film
        counted_movies = dict()
        for user in users:
            for movie in self.get_movies_from_user(user):
                if movie in counted_movies:
                    counted_movies[movie] += 1
                else:
                    counted_movies[movie] = 1
        # Transforme le dictionnaire en liste pour pouvoir le trier
        counted_movies_list = [(counted_movies[key], key) for key in counted_movies.keys()]
        # Trie la liste de film par nombre d'occurences décroissant
        counted_movies_list.sort()
        counted_movies_list.reverse()
        # Récupère seulement le nom des films
        best_movies_list = [value for (key, value) in counted_movies_list]
        return best_movies_list

    # Affiche la recommandation pour l'utilisateur
    def make_recommendation(self, user):
        # Tri les utilisateurs par similarité
        similarities = self.compute_all_similarities(user)
        similarities.sort()
        similarities.reverse()

        # Récupère les 5 utilisateurs les plus similaires
        most_similar_user_ids = [user_id for similarity, user_id in similarities[0:5]]
        most_similar_users = [self.test_users[user_id] for user_id in most_similar_user_ids]
        # Prend les 3 films qui correspondent le mieux
        recommendations = self.get_best_movies_from_users(most_similar_users)[0:3]

        # Réinitialise la question de l'utilisateur
        user.latest_movie_asked = None
        user.questions_before_recommendation = None

        return "Vos recommandations : " + ", ".join(recommendations)

    # Calcule la similarité entre 2 utilisateurs
    @staticmethod
    def get_similarity(user_a, user_b):
        score = 0
        for good_rating in user_a.good_ratings:
            if good_rating in user_b.good_ratings:
                score += 1
            if good_rating in user_b.bad_ratings:
                score -= 1
        for bad_rating in user_a.bad_ratings:
            if bad_rating in user_b.bad_ratings:
                score += 1
            if bad_rating in user_b.good_ratings:
                score -= 1

        norm_a = user_a.get_norm()
        norm_b = user_b.get_norm()

        return score / (norm_a * norm_b)

    # Calcule la similarité entre un utilisateur et tous les utilisateurs de tests
    def compute_all_similarities(self, user):
        similarities = []
        for other_user in self.test_users.values():
            similarities.append((self.get_similarity(user, other_user), other_user.id))
        return similarities
