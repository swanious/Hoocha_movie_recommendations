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
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=100)
    movies = models.ManyToManyField(Movie, related_name='genres') # 중계모델


class MovieReview(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_reviews')

    title = models.CharField(max_length=50)
    content = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


class MovieReviewComment(models.Model):
    movie_review = models.ForeignKey(MovieReview, on_delete=models.CASCADE, related_name='movie_review_comments')

    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    


class MovieOneline(models.Model):
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE, related_name='movie_onelines')

    content = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    
