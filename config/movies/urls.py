from django.urls import path
from . import views

app_name = 'movies'

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:movie_id>/', views.detail, name='detail'),

    # # movie_review
    path('<int:movie_id>/movie_review_list/', views.movie_review_list, name='movie_review_list'),
    path('<int:movie_id>/movie_review/create/', views.movie_review_create, name='movie_review_create'),
    path('<int:movie_id>/movie_review/<int:movie_review_id>/', views.movie_review_detail, name='movie_review_detail'),
    # path('<int:movie_id>/movie_review/<int:movie_review_id>/update/', views.movie_review_update, name='movie_review_update'),
    # path('<int:movie_id>/movie_review/<int:movie_review_id>/delete/', views.movie_review_delete, name='movie_review_delete'),
    
    # # movie_review_comment
    # path('<int:movie_id>/movie_review/<int:movie_review_id>/movie_review_comment_create/', views.movie_review_comment_create, name='movie_review_comment_create'),
    # path('<int:movie_id>/movie_review/<int:movie_review_id>/movie_review_comment_update/', views.movie_review_comment_update, name='movie_review_comment_update'),
    # path('<int:movie_id>/movie_review/<int:movie_review_id>/movie_review_comment_delete/', views.movie_review_comment_delete, name='movie_review_comment_delete'),


    # # movie_oneline_comment
    # path('<int:movie_id>/movie_oneline_comment/', views.movie_oneline_comment, name='movie_oneline_comment'),
    # path('<int:movie_id>/movie_oneline_comment/create/', views.movie_oneline_comment_create, name='movie_oneline_comment_create'),
    # path('<int:movie_id>/movie_oneline_comment/<int:movie_oneline_comment_id>/update/', views.movie_oneline_comment_update, name='movie_oneline_comment_update'),
    # path('<int:movie_id>/movie_oneline_comment/<int:movie_oneline_comment_id>/delete/', views.movie_oneline_comment_delete, name='movie_oneline_comment_delete'),

    path('data/', views.tmdb, name='data'),
]
