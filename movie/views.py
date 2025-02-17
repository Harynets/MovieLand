from django.shortcuts import render
from decouple import config
import tmdbsimple as tmdb


def index(request):
    tmdb.API_KEY = config("TMDB_API_KEY")
    popular = tmdb.Movies().popular(language="uk-UA")["results"]

    context = {
        "popular": popular[:12]
    }
    return render(request, "movie/index.html", context)
