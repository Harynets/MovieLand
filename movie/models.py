from django.contrib.auth.models import User
from django.db import models

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_review = models.TextField()
    date = models.DateTimeField(auto_now=True)
    rating = models.SmallIntegerField()
    movie_id = models.PositiveIntegerField()
