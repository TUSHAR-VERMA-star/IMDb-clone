from codecs import oem_decode
from operator import mod
from platform import platform
from venv import create
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.contrib.auth.models import User


# Create your models here.


class StreamPlatform(models.Model):
    name = models.CharField(max_length=50)
    about = models.CharField(max_length=100)
    link = models.URLField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Watchlist(models.Model):
    title = models.CharField(max_length=50)
    storyline = models.CharField(max_length=100)
    active = models.BooleanField(default=True)
    platform = models.ForeignKey(
        StreamPlatform, on_delete=models.CASCADE, related_name="watchlist")
    avg_rating = models.FloatField(default=0)
    number_rating = models.IntegerField(default=0)
    create = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.title

class Review(models.Model):
    review_user = models.ForeignKey(User, on_delete=models.CASCADE)
    rating = models.PositiveIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    description = models.CharField(max_length=200, null=True)
    watchlist = models.ForeignKey(Watchlist, on_delete=models.CASCADE, related_name="reviews")
    active = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating) + " | " + self.watchlist.title 