from django.contrib import admin
from .models import Movie,Genre,Review,Comment,Oneline

# Register your models here.
admin.site.register(Movie)
admin.site.register(Genre)
admin.site.register(Review)
admin.site.register(Comment)
admin.site.register(Oneline)
