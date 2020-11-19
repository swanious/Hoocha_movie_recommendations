from django.db import models


# Create your models here.
class Movie(models.Model):
    id = models.IntegerField(primary_key=True)
    popularity = models.FloatField()
    video = models.BooleanField(default=False)
    vote_count = models.IntegerField()
    vote_average = models.FloatField()
    title = models.CharField(max_length=50)
    release_date = models.DateField()
    original_language = models.CharField(max_length=2)
    original_title = models.CharField(max_length=100)
    backdrop_path = models.TextField(blank=True)
    adult = models.BooleanField(default=False)
    overview = models.TextField()
    poster_path = models.TextField()


class Genre(models.Model):
    movies = models.ManyToManyField(Movie, related_name='genres') # 중계모델
    name = models.CharField(max_length=100)


# class Moive_Gerne:
# 
