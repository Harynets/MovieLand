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


def person(request, person_id, person_slug):
    tmdb.API_KEY = config("TMDB_API_KEY")

    # check if person_id exists
    try:
        person_ = tmdb.People(person_id)

        # correct slug in the url if it is wrong
        if (correct_person_slug := slugify(tmdb.People(person_id).info()["name"])) != person_slug:
           return redirect('movie:person', person_id=person_id, person_slug=correct_person_slug)

    except requests.exceptions.HTTPError:
        raise Http404("Person is not found")

    persons_movies = person_.movie_credits(language="uk-UA")

    filmography = dict.fromkeys({dict_["department"] for dict_ in persons_movies["crew"]}, [])

    # add movies in which person has crew role
    for movie_ in persons_movies["crew"]:
        if movie_.get("poster_path") and movie_.get("release_date"):
            filmography[movie_["department"]].append(movie_)

    # add movies in which person has acting role
    if persons_movies["cast"]:
        filmography["Acting"] = [item for item in persons_movies["cast"] if item.get("poster_path") and item.get("release_date")]
    # sort each movie in category by movie release date
    filmography = {key: sorted(value, key=lambda item: item["release_date"], reverse=True) for key, value in filmography.items()}

    context = {
        "person": person_.info(language="uk-UA"),
        "filmography": dict(sorted(filmography.items(), key=lambda item: len(item[1]), reverse = True))
    }

    return render(request, "movie/person.html", context)