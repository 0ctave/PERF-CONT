import json
import os
from dotenv import load_dotenv
from pathlib import Path
import requests

from flask import request
from graphql import GraphQLError

dotenv_path = Path('../.env')
load_dotenv(dotenv_path=dotenv_path)
IMDB_API_KEY = os.getenv('IMDB_KEY')
IMDB_LINK = f"https://imdb-api.com/en/API/"


def movie_by_id_imdb(_id: str):
    try:
        link = IMDB_LINK + f"Title/{IMDB_API_KEY}/" + _id
        movie = json.loads(requests.get(link).text)
        res = {
            "director": movie["directors"],
            "rating": movie["imDbRating"],
            "title": movie["title"],
            "id": movie["id"]
        }
        return res
    except KeyError:
        return None


def movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['id'] == _id:
                return movie

        imdb = movie_by_id_imdb(_id)
        print(imdb)
        if imdb != None: return imdb

        raise GraphQLError('ID not found')


def movie_with_title(_, info, _title):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['title'] == _title:
                return movie
        raise GraphQLError('title not found')


def movie_with_director(_, info, _director):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie['director'] == _director:
                return movie
        raise GraphQLError('director not found')


def create_movie(_, info, _id, _title, _rating, _director):
    with open('{}/data/movies.json'.format("."), "r+") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie["id"] == _id:
                raise GraphQLError('movie ID already exists')
        movie = {"id": _id, "director": _director, "title": _title, "rating": _rating}
        file.seek(0)
        file.truncate()
        movies['movies'].append(movie)
        json.dump(movies, file,
                  indent=4,
                  separators=(',', ': '))
        return movie


def update_movie_rate(_, info, _id, _rate):
    newmovies = {}
    newmovie = {}
    with open('{}/data/movies.json'.format("."), "r") as rfile:
        movies = json.load(rfile)
        for movie in movies['movies']:
            if movie['id'] == _id:
                movie['rating'] = _rate
                newmovie = movie
                newmovies = movies
    with open('{}/data/movies.json'.format("."), "w") as wfile:
        json.dump(newmovies, wfile)
    return newmovie


def del_movie_with_id(_, info, _id):
    with open('{}/data/movies.json'.format("."), "r+") as file:
        movies = json.load(file)
        for movie in movies['movies']:
            if movie["id"] == _id:
                movies['movies'].remove(movie)
                file.seek(0)
                json.dump(movies, file,
                          indent=4,
                          separators=(',', ': '))
                file.truncate()
                return movie
        raise GraphQLError('ID not found')


def movies_rate_above_rating(_, info, _rating):
    with open('{}/data/movies.json'.format("."), "r") as file:
        movies = json.load(file)
        movie_list = []
        for movie in movies['movies']:
            if float(movie["rating"]) >= _rating:
                movie_list.append(movie)
        return movie_list


def resolve_actors_in_movie(movie, info):
    with open('{}/data/actors.json'.format("."), "r") as file:
        data = json.load(file)
        actors = [actor for actor in data['actors'] if movie['id'] in actor['films']]
        return actors


def actor_with_id(_, info, _id):
    with open('{}/data/actors.json'.format("."), "r") as file:
        actors = json.load(file)
        for actor in actors['actors']:
            if actor['id'] == _id:
                return actor
        raise GraphQLError('ID not found')
