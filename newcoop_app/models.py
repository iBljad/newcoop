from django.contrib.auth.models import User
from django.db import models


class Platform(models.Model):
    platform_name = models.CharField(max_length=50)

    def __str__(self):
        return self.platform_name

    class Meta:
        ordering = ['platform_name']


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

    class Meta:
        ordering = ['-pub_date']


class Link(models.Model):
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.CASCADE)

    def __str__(self):
        return '%s — %s' % (self.game.game_name, self.platform.platform_name)


class GameRequest(models.Model):
    COOP_TEAMMATE = 1
    SQUAD = 2
    CLAN_MEMBER = 3
    COMPETITOR = 4

    REQUEST_TYPE_CHOICES = [
        (COOP_TEAMMATE, 'Co-op teammate'),
        (SQUAD, 'Squad member'),
        (CLAN_MEMBER, 'Clan member'),
        (COMPETITOR, 'Competitor')
    ]

    RU = 1
    EN = 2
    Other = 3

    LANG_CHOICES = [
        (RU, 'Russian'),
        (EN, 'English'),
        (Other, 'Other')
    ]

    active = models.BooleanField(default=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    game = models.ForeignKey(Game, on_delete=models.CASCADE)
    platform = models.ForeignKey(Platform, on_delete=models.SET_NULL, blank=True, null=True)
    pub_date = models.DateTimeField('post published', auto_now=True)
    mic_present = models.BooleanField(default=False)
    language = models.IntegerField(choices=LANG_CHOICES)
    # language = models.ForeignKey(Language, on_delete=models.SET_NULL, blank=True, null=True)
    request_type = models.IntegerField(choices=REQUEST_TYPE_CHOICES)
    comment = models.TextField(max_length=400, blank=True)

    def __str__(self):
        return '%s by %s at %s' % (self.game, self.user, self.pub_date.date())

    def comments_count(self):
        return self.requestcomment_set.filter(active=True).count()


class RequestLikes(models.Model):
    request = models.ForeignKey(GameRequest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    liked = models.BooleanField()
    pub_date = models.DateTimeField('post published', auto_now=True)

    class Meta:
        unique_together = ('request', 'user',)

    def __str__(self):
        return "%s by %s at %s" % (self.liked, self.user, self.pub_date)


class RequestComment(models.Model):
    active = models.BooleanField(default=True)
    request = models.ForeignKey(GameRequest, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.TextField(max_length=400, blank=True)
    pub_date = models.DateTimeField('post published', auto_now=True)

    def __str__(self):
        return "%s by %s at %s" % (self.comment[:20], self.user, self.pub_date)
