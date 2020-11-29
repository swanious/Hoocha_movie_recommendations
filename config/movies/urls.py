from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('data/', views.tmdb, name='data'),
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),

    # review
    path('<int:movie_id>/review_list/', views.review_list, name='review_list'),
    path('<int:movie_id>/review/create/', views.review_create, name='review_create'),
    path('<int:movie_id>/review/<int:review_id>/', views.review_detail, name='review_detail'),
    path('<int:movie_id>/review/<int:review_id>/update/', views.review_update, name='review_update'),
    path('<int:movie_id>/review/<int:review_id>/delete/', views.review_delete, name='review_delete'),
    path('<int:movie_id>/review/<int:review_id>/like/', views.review_like, name='review_like'),
    
    # comment
    path('<int:movie_id>/review/<int:review_id>/comment_create/', views.comment_create, name='comment_create'),
    path('<int:movie_id>/review/<int:review_id>/comment/<int:comment_id>/update/', views.comment_update, name='comment_update'),
    path('<int:movie_id>/review/<int:review_id>/comment/<int:comment_id>/delete/', views.comment_delete, name='comment_delete'),

    # oneline
    path('<int:movie_id>/oneline/', views.oneline_list, name='oneline_list'),
    path('<int:movie_id>/oneline/create/', views.oneline_create, name='oneline_create'),
    path('<int:movie_id>/oneline/<int:oneline_id>/update/', views.oneline_update, name='oneline_update'),
    path('<int:movie_id>/oneline/<int:oneline_id>/delete/', views.oneline_delete, name='oneline_delete'),
    path('<int:movie_id>/oneline/<int:oneline_id>/like/', views.oneline_like, name='oneline_like'),
]
