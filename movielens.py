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
            if genre == "Action":
                self.action = 1
            if genre == "Adventure":
                self.adventure = 1
            if genre == "Animation":
                self.animation = 1
            if genre == "Children":
                self.children = 1
            if genre == "Comedy":
                self.comedy = 1
            if genre == "Crime":
                self.crime = 1
            if genre == "Documentary":
                self.documentary = 1
            if genre == "Drama":
                self.drama = 1
            if genre == "Fantasy":
                self.fantasy = 1
            if genre == "Film-Noir":
                self.film_noir = 1
            if genre == "Horror":
                self.horror = 1
            if genre == "Musical":
                self.musical = 1
            if genre == "Mystery":
                self.mystery = 1
            if genre == "Romance":
                self.romance = 1
            if genre == "Sci-Fi":
                self.sci_fi = 1
            if genre == "Thriller":
                self.thriller = 1
            if genre == "War":
                self.war = 1
            if genre == "Western":
                self.western = 1


def load_movies():
    movies = []
    with open('./ml-latest-small/movies-popular.csv', 'rt', encoding="utf-8") as moviesFile:
        raw_movies = csv.reader(moviesFile, delimiter=',')
        is_first = True
        for movie in raw_movies:
            if is_first:
                is_first = False
                continue
            movies.append(Movie(movie[0], movie[1], movie[2], movie[3]))

    return movies


class Rating:

    def __init__(self, movie_id, user_id, score=None, is_appreciated=None):
        self.movie = int(movie_id)
        self.user = int(user_id)
        self.score = float(score) if score is not None else None
        self.is_appreciated = bool(is_appreciated) if is_appreciated is not None else None


def load_simplified_ratings():
    ratings = []
    with open('./ml-latest-small/ratings-popular-simplified.csv', 'rt', encoding="utf-8") as ratingsFile:
        raw_ratings = csv.reader(ratingsFile, delimiter=',')
        is_first = True
        for rating in raw_ratings:
            if is_first:
                is_first = False
                continue
            ratings.append(Rating(rating[1], rating[0], None, rating[2]))

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
            ratings.append(Rating(rating[1], rating[0], rating[2], None))

    return ratings
