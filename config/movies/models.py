from django.db import models
from django.conf import settings


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
    
    watch_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='watch_movies')


class Genre(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, related_name='genres') # 중계모델


class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='reviews')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_reviews')

    title = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name='comments')

    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    


class Oneline(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='onelines')
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_onelines')

    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    

