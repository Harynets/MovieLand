from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('', views.index, name="index"),
    path('movie/<int:movie_id>-<slug:movie_slug>/', views.movie, name="movie"),
    path('person/<int:person_id>-<slug:person_slug>/', views.person, name="person"),
]