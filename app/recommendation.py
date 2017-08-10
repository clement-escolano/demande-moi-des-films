# coding: utf-8

# All the recommandation logic and algorithms goes here

from app.User import User


class Recommendation:

    def __init__(self, movielens):

        # Dictionary of movies
        # The structure of a movie is the following:
        #     * id (which is the movie number, you can access to the movie with "self.movies[movie_id]")
        #     * title
        #     * release_date (year when the movie first aired)
        #     * adventure (=1 if the movie is about an adventure, =0 otherwise)
        #     * drama (=1 if the movie is about a drama, =0 otherwise)
        #     * ... (the list of genres)
        self.movies = movielens.movies

        # List of ratings
        # The structure of a rating is the following:
        #     * movie (with the movie number)
        #     * user (with the user number)
        #     * is_appreciated (in the case of simplified rating, whether or not the user liked the movie)
        #     * score (in the case of rating, the score given by the user)
        self.ratings = movielens.simplified_ratings

        # This is the set of users in the training set
        self.test_users = {}

        # Launch the process of ratings
        self.process_ratings_to_users()

    # To process ratings, users associated to ratings are created and every rating is then stored in its user
    def process_ratings_to_users(self):
        for rating in self.ratings:
            user = self.register_test_user(rating.user)
            movie = self.movies[rating.movie]
            if rating.is_appreciated is not None:
                if rating.is_appreciated:
                    user.good_ratings.append(movie)
                else:
                    user.bad_ratings.append(movie)
            elif rating.score is not None:
                user.ratings.append(movie)

    # Register a user if it does not exist and return it
    def register_test_user(self, sender):
        if sender not in self.test_users.keys():
            self.test_users[sender] = User(sender)
        return self.test_users[sender]

    # Display the recommendation for a user
    def make_recommendation(self, user):
        # Sort users by similarity
        similarities = self.compute_all_similarities(user)
        similarities.sort()
        similarities.reverse()

        # Get the 5 most similar users
        most_similar_user_ids = [user_id for similarity, user_id in similarities[0:5]]
        most_similar_users = [self.test_users[user_id] for user_id in most_similar_user_ids]
        # Get the 3 movies that are most common among the 5 users
        recommendations = self.get_best_movies_from_users(most_similar_users)[0:3]

        return "Vos recommandations : " + ", ".join(recommendations)

    # Compute the similarity between two users
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

        norm_a = Recommendation.get_user_norm(user_a)
        norm_b = Recommendation.get_user_norm(user_b)

        return score / (norm_a * norm_b)

    # Compute the similarity between a user and all the users in the data set
    def compute_all_similarities(self, user):
        similarities = []
        for other_user in self.test_users.values():
            similarities.append((self.get_similarity(user, other_user), other_user.id))
        return similarities

    @staticmethod
    def get_best_movies_from_users(users):
        # Dictionary with the number of occurences of every movie
        counted_movies = dict()
        for user in users:
            for movie in Recommendation.get_user_appreciated_movies(user):
                if movie in counted_movies:
                    counted_movies[movie] += 1
                else:
                    counted_movies[movie] = 1
        # Transform the dictionary in list to sort it
        counted_movies_list = [(counted_movies[key], key) for key in counted_movies.keys()]
        # Sort the list
        counted_movies_list.sort()
        counted_movies_list.reverse()
        # Get only the movies title
        best_movies_list = [value for (key, value) in counted_movies_list]
        return best_movies_list

    @staticmethod
    def get_user_appreciated_movies(user):
        movies_list = []
        good_movies = user.good_ratings
        for movie in good_movies:
            movies_list.append(movie.title)
        return movies_list

    @staticmethod
    def get_user_norm(user):
        return 1 + len(user.good_ratings) + len(user.bad_ratings)

    # Return a vector with the normalised ratings of a user
    @staticmethod
    def get_normalised_cluster_notations(user):
        return []
