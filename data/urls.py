from django.urls import path
from . import views

name="data"

urlpatterns = [
    # path('', views.naver), 
    # path('', views.kofic), 
    path('', views.tmdb), 
]
