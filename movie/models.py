from django.contrib.auth.models import User
from django.db import models
from django_resized import ResizedImageField

class Review(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text_review = models.TextField()
    date = models.DateTimeField(auto_now=True)
    rating = models.SmallIntegerField()
    movie_id = models.PositiveIntegerField()

    def __str__(self):
        return f"user: {self.user}, review: {self.text_review}, date: {self.date}, rating: {self.rating}, movie id: {self.movie_id}"


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = ResizedImageField(size=[1280, 1280], crop=['middle', 'center'], blank=True, default="profile_images/default_profile_image.png", upload_to="profile_images/")

    def __str__(self):
        return f"{self.profile_image}"
