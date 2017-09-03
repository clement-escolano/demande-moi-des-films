# Utilities to process movies and ratings.
# They will output only popular and recent movies for a better experience.

import re
import csv

year_regex = re.compile('\d{4}')
title_regex = re.compile('(.*)\(\d{4}\)')


def get_movie_year(movie):
    match = year_regex.search(movie)
    if match is None:
        return None
    return int(match.group(0))


def get_appreciation(score):
    score = float(score)
    if score >= 4:
        return True
    if score <= 2:
        return False
    return None


def transform_movies():
    movies_list = []
    movies_file = open('./ml-latest-small/movies.csv', 'rt')
    movies = csv.reader(movies_file, delimiter=',')
    is_first = True
    movies_list.append(["id", "title", "year", "genre"])
    for movie in movies:
        if is_first:
            is_first = False
            continue
        year = get_movie_year(movie[1])
        title = title_regex.match(movie[1]).group(1).strip() if year else movie[1]
        movies_list.append([int(movie[0]), title, year, movie[2]])

    popular_movies_file = open('./ml-latest-small/movies-clean.csv', 'wt')
    popular_movies_writer = csv.writer(popular_movies_file, delimiter=',')
    for row in movies_list:
        popular_movies_writer.writerow(row)

    movies_dict = dict()
    is_first = True
    for movie in movies_list:
        if is_first:
            is_first = False
            continue
        movies_dict[movie[0]] = movie

    return movies_dict


def transform_ratings(movies_dict):
    ratings_list = []
    popular_ratings = []
    movies_occurences = dict()

    ratings_file = open('./ml-latest-small/ratings.csv', 'rt')
    ratings = csv.reader(ratings_file, delimiter=',')
    is_first = True
    for rating in ratings:
        if is_first:
            is_first = False
            continue
        is_appreciated = get_appreciation(rating[2])
        if is_appreciated is not None:
            ratings_list.append([int(rating[0]), int(rating[1]), rating[2]])
    for rating in ratings_list:
        movie = rating[1]
        if movie in movies_occurences:
            movies_occurences[movie] += 1
        else:
            movies_occurences[movie] = 1

    popular_ratings.append(["user", "movie", "score"])
    for rating in ratings_list:
        if movies_occurences[rating[1]] > 25 and movies_dict[rating[1]][2] > 2000:
            popular_ratings.append(rating)

    popular_ratings_file = open('./ml-latest-small/ratings-popular.csv', 'wt')
    popular_ratings_writer = csv.writer(popular_ratings_file, delimiter=',')
    for row in popular_ratings:
        popular_ratings_writer.writerow(row)


movies = transform_movies()
transform_ratings(movies)
