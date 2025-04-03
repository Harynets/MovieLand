import requests
from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from decouple import config
import tmdbsimple as tmdb
from django.urls import reverse_lazy
from django.utils.text import slugify
from django.views.generic import CreateView
from movie.forms import *
from movie.models import *


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
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            form_data = review_form.cleaned_data
            Review(user=request.user, movie_id=movie_id, **form_data).save()
            return redirect(request.path)
    else:
        review_form = ReviewForm()

    tmdb.API_KEY = config("TMDB_API_KEY")

    # check if movie_id exists
    try:
        movie_ = tmdb.Movies(movie_id)

        # correct slug in the url if it is wrong
        if (correct_movie_slug := slugify(tmdb.Movies(movie_id).info()["title"])) != movie_slug:
           return redirect('movie:movie', movie_id=movie_id, movie_slug=correct_movie_slug)

    except requests.exceptions.HTTPError:
        raise Http404("Movie is not found")

    # get all reviews except review that written by user that requested page
    reviews = Review.objects.all().filter(movie_id=movie_id).exclude(user=request.user if request.user.is_authenticated else None).values("user__username", "user__profileuser__profile_image", "rating", "text_review", "date")

    # get director and screenplay
    crew = {item["job"]: item for item in movie_.credits()["crew"] if item["job"] == "Director" or item["job"] == "Screenplay"}

    # get review written by user that requested page
    current_user_review = None
    if Review.objects.filter(user=request.user.id, movie_id=movie_id).exists():
        current_user_review = Review.objects.filter(user=request.user.id, movie_id=movie_id).values("rating", "text_review", "date")
    
    context = {
        "movie": movie_.info(language="uk-UA"),
        "cast": movie_.credits(language="uk-UA")["cast"][:12],
        "crew": crew,
        "similar_movies": movie_.similar_movies(language="uk-UA")["results"][:12],
        "form": review_form,
        "reviews": reviews,
        "current_user_review": current_user_review
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


class RegisterUser(CreateView):
    form_class = RegisterUserForm
    template_name = "movie/register.html"
    success_url = reverse_lazy("movie:index")

    def form_valid(self, form):
        user = form.save()  # add new user to database
        login(self.request, user)  # auto login
        return redirect("movie:index")


class LoginUser(LoginView):
    form_class = AuthenticationUserForm
    template_name = "movie/login.html"

    def get_success_url(self):
        return reverse_lazy("movie:index")


def logout_user(request):
    logout(request)
    return redirect("movie:login")

def profile(request, username):
    if request.method == "POST":
        form = ProfileUserForm(request.POST, request.FILES)
        if form.is_valid():
            profile_user, created = ProfileUser.objects.get_or_create(user=request.user)
            profile_user.profile_image = request.FILES["profile_image"]
            profile_user.save()
        return redirect("movie:profile", username=username)

    tmdb.API_KEY = config("TMDB_API_KEY")
    user = get_object_or_404(User.objects.filter(username=username))
    user_reviews = Review.objects.filter(user=user).order_by("-date").values()
    number_of_reviews = len(user_reviews)
    for review in user_reviews[:3]:
        movie_ = tmdb.Movies(review["movie_id"]).info(language="uk-UA")
        review["movie_name"] = movie_["title"]
        review["poster_path"] = movie_["poster_path"]

    # try to get user profile image
    profile_image = ProfileUser.objects.filter(user=user).values().first()
    # if no image return None else return image
    profile_image = profile_image and profile_image["profile_image"]

    context = {
        "profile_user":user,
        "user_reviews": user_reviews[:3],
        "number_of_reviews": number_of_reviews,
        "profile_image": profile_image,
        "form": ProfileUserForm()
    }
    return render(request, "movie/profile.html", context)
