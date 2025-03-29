from django.urls import path
from . import views

app_name = "movie"

urlpatterns = [
    path('', views.index, name="index"),
    path('movie/<int:movie_id>-<slug:movie_slug>/', views.movie, name="movie"),
    path('person/<int:person_id>-<slug:person_slug>/', views.person, name="person"),
    path('register/', views.RegisterUser.as_view(), name="register"),
    path('login/', views.LoginUser.as_view(), name="login"),
    path('logout/', views.logout_user, name="logout"),
    path('profile/<slug:username>/', views.profile, name="profile"),
]