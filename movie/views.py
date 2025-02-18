import requests
from django.http import Http404
from django.shortcuts import render, redirect
from decouple import config
import tmdbsimple as tmdb
from django.utils.text import slugify


def index(request):
    tmdb.API_KEY = config("TMDB_API_KEY")
    popular = tmdb.Movies().popular(language="uk-UA")["results"]
    english_popular = tmdb.Movies().popular()["results"] # used for generating slug from title

    context = {
        "popular": [{"title": item["title"],
                     "poster_path": item["poster_path"],
                     "slug": slugify(english_popular[index]["title"]),
                     "id": item["id"]}
                     for index, item in enumerate(popular)][:12]
    }

    return render(request, "movie/index.html", context)


def movie(request, movie_id, movie_slug):
    tmdb.API_KEY = config("TMDB_API_KEY")

    # check if movie_id exists
    try:
        movie_ = tmdb.Movies(movie_id)

        # correct slug in the url if it is wrong
        if (correct_movie_slug := slugify(tmdb.Movies(movie_id).info()["title"])) != movie_slug:
           return redirect('movie:movie', movie_id=movie_id, movie_slug=correct_movie_slug)

    except requests.exceptions.HTTPError:
        raise Http404("Movie is not found")

    context = {
        "movie": movie_.info(language="uk-UA"),
        "cast": movie_.credits(language="uk-UA")["cast"][:12],
    }

    return render(request, "movie/movie.html", context)
