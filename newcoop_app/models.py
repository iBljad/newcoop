from django.contrib.auth.models import User
from django.db import models


class Platform(models.Model):
    platform_name = models.CharField(max_length=50)

    def __str__(self):
        return self.platform_name


class Genre(models.Model):
    genre_name = models.CharField(max_length=100)

    def __str__(self):
        return self.genre_name


class Game(models.Model):
    game_name = models.CharField(max_length=200)
    pub_date = models.DateField('release date', blank=True)
    genre = models.ForeignKey(Genre, on_delete=models.SET_NULL, blank=True, null=True)

    def __str__(self):
        return self.game_name


class Language(models.Model):
    lang_code = models.CharField(max_length=10)

    def __str__(self):
        return self.lang_code


class GameRequest(models.Model):
    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, blank=True, null=True)
    pub_date = models.DateTimeField('post published', auto_now=True)
    mic_present = models.BooleanField(default=False)
    language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    comment = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return "%s by %s at %s" % (self.game, self.user, self.pub_date)


class RequestLikes(models.Model):
    request = models.ForeignKey(GameRequest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField
    pub_date = models.DateTimeField('post published', auto_now=True)

    def __str__(self):
        return "%s by %s at %s" % (self.liked, self.user, self.pub_date)


class RequestComment(models.Model):
    request = models.ForeignKey(GameRequest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=400, blank=True)
    pub_date = models.DateTimeField('post published', auto_now=True)

    def __str__(self):
        return "%s by %s at %s" % (self.comment[:20], self.user, self.pub_date)
