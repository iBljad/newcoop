from django.contrib.auth.models import User
from django.db import models


class Platform(models.Model):
    platform_name = models.CharField(max_length=50)


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)


class Game(models.Model):
    game_name = models.CharField(max_length=200)
    pub_date = models.DateTimeField('release date', blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)


class Language(models.Model):
    lang_code = models.CharField(max_length=10)


class GameRequest(models.Model):
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, blank=True, null=True)
    pub_date = models.DateTimeField('post published', auto_now=True)
    mic_present = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(max_length=400, blank=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
