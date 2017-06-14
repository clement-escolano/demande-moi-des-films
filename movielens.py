import csv


class Movie:

    def __init__(self, movie_id, title, release_date, genres):
        self.id = int(movie_id)
        self.title = title
        self.release_date = release_date
        self.unknown = 0
        self.action = 0
        self.adventure = 0
        self.animation = 0
        self.children = 0
        self.comedy = 0
        self.crime = 0
        self.documentary = 0
        self.drama = 0
        self.fantasy = 0
        self.film_noir = 0
        self.horror = 0
        self.musical = 0
        self.mystery = 0
        self.romance = 0
        self.sci_fi = 0
        self.thriller = 0
        self.war = 0
        self.western = 0

        self.init_genres(genres)

    def init_genres(self, genres):
        for genre in genres.split('|'):
            if genre is "Action":
                self.action = 1
            if genre is "Adventure":
                self.adventure = 1
            if genre is "Animation":
                self.animation = 1
            if genre is "Children":
                self.children = 1
            if genre is "Comedy":
                self.comedy = 1
            if genre is "Crime":
                self.crime = 1
            if genre is "Documentary":
                self.documentary = 1
            if genre is "Drama":
                self.drama = 1
            if genre is "Fantasy":
                self.fantasy = 1
            if genre is "Film-Noir":
                self.film_noir = 1
            if genre is "Horror":
                self.horror = 1
            if genre is "Musical":
                self.musical = 1
            if genre is "Mystery":
                self.mystery = 1
            if genre is "Romance":
                self.romance = 1
            if genre is "Sci-Fi":
                self.sci_fi = 1
            if genre is "Thriller":
                self.thriller = 1
            if genre is "War":
                self.war = 1
            if genre is "Western":
                self.western = 1


def load_movies():
    movies = dict()
    with open('./ml-latest-small/movies-popular.csv', 'rt', encoding="utf-8") as moviesFile:
        raw_movies = csv.reader(moviesFile, delimiter=',')
        is_first = True
        for movie in raw_movies:
            if is_first:
                is_first = False
                continue
            movies[int(movie[0])] = Movie(movie[0], movie[1], movie[2], movie[3])

    return movies


class Rating:

    def __init__(self, movie_id, user_id, score=0, is_appreciated="True"):
        self.movie = int(movie_id)
        self.user = int(user_id)
        self.score = float(score)
        self.is_appreciated = bool(is_appreciated)


def load_simplified_ratings():
    ratings = []
    with open('./ml-latest-small/ratings-popular-simplified.csv', 'rt', encoding="utf-8") as ratingsFile:
        raw_ratings = csv.reader(ratingsFile, delimiter=',')
        is_first = True
        for rating in raw_ratings:
            if is_first:
                is_first = False
                continue
            ratings.append(Rating(rating[1], rating[0], 0, rating[2]))

    return ratings


def load_ratings():
    ratings = []
    with open('./ml-latest-small/ratings-popular.csv', 'rt', encoding="utf-8") as ratingsFile:
        raw_ratings = csv.reader(ratingsFile, delimiter=',')
        is_first = True
        for rating in raw_ratings:
            if is_first:
                is_first = False
                continue
            ratings.append(Rating(rating[1], rating[0], rating[2]))

    return ratings
