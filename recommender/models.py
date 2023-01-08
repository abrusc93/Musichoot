from django.db import models
from django.contrib.auth.models import User

class Musicdata(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter()

    acousticness = models.FloatField()
    artists = models.TextField()
    danceability = models.FloatField()
    duration_ms = models.FloatField()
    energy = models.FloatField()
    explicit = models.FloatField()
    id = models.TextField(primary_key=True)
    instrumentalness = models.FloatField()
    key = models.FloatField()
    liveness = models.FloatField()
    loudness = models.FloatField()
    mode = models.FloatField()
    name = models.TextField()
    popularity = models.FloatField()
    release_date = models.TextField(null=True)
    speechiness = models.FloatField()
    tempo = models.FloatField()
    valence = models.FloatField()
    year = models.IntegerField()
    likes = models.ManyToManyField(User, related_name='like', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')
    objects = models.Manager()  # default manager
    newmanager = NewManager()  # custom manager

class Playlist(models.Model):

    class NewManager(models.Manager):
        def get_queryset(self):
            return super().get_queryset() .filter()

    title = models.TextField()
    owner = models.ManyToManyField(User, related_name='userid')
    songs = models.ManyToManyField(Musicdata, related_name='song', default=None)
    is_public = models.BooleanField(default=True)
    objects = models.Manager()                      #Default manager
    newmanager = NewManager()
    likes = models.ManyToManyField(User, related_name='like_playlist', default=None, blank=True)
    like_count = models.BigIntegerField(default='0')