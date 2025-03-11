from django.contrib.auth.models import User
from django.db import models

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_review = models.TextField()
    date = models.DateTimeField(auto_now=True)
    rating = models.SmallIntegerField()
    movie_id = models.PositiveIntegerField()

    def __str__(self):
        return f"user: {self.user}, review: {self.text_review}, date: {self.date}, rating: {self.rating}, movie id: {self.movie_id}"