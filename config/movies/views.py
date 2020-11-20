from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods

from django.contrib.auth.decorators import login_required

from .models import Movie, Genre, MovieReview, MovieReviewComment, MovieOneline
from .forms import MovieReviewForm, MovieReviewCommentForm, MovieOnelineForm

import requests


@require_http_methods(['GET'])
def index(request):
    movies = Movie.objects.all()
    context = {
        'movies': movies,
    }
    return render(request, 'movies/index.html', context)


@require_http_methods(['GET'])
def detail(request, movie_id):
    movie = get_object_or_404(Movie, id=movie_id)
    context = {
        'movie': movie,
    }
    return render(request, 'movies/detail.html', context)


def movie_review_list(request, movie_id):
    # articles = Article.objects.prefetch_related('like_users').select_related('user').annotate(likes=Count('like_users')).order_by('-pk')
    movie = get_object_or_404(Movie, id=movie_id)
    movie_reviews = movie.movie_reviews.all()
    context = {
        'movie_reviews': movie_reviews,
    }
    return render(request, 'movies/movie_review_list.html', context)


# @login_required
@require_http_methods(['GET', 'POST'])
def movie_review_create(request, movie_id):
    if request.method == 'POST':
        form = MovieReviewForm(request.POST) 
        if form.is_valid():
            movie_review = form.save(commit=False)
            movie = get_object_or_404(Movie, id=movie_id)
            movie_review.movie = movie
            # movie_review.user = request.user
            movie_review.save()
            return redirect('movies:movie_review_list', movie_id)
    else:
        form = MovieReviewForm()
    context = {
        'form': form,
    }
    return render(request, 'movies/movie_review_create.html', context)



def movie_review_detail(request, movie_id, movie_review_id):
    movie = get_object_or_404(Movie, id=movie_id)
    movie_review = get_object_or_404(MovieReview, id=movie_review_id)
    # comment_form = CommentForm()
    # comments = movies.movie_reviews.all()
    context = {
        'movie_review': movie_review,
        # 'comment_form': comment_form,
        # 'comments': comments,
    }
    return render(request, 'movies/movie_review_detail.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def movie_review_update(request, pk):
    # article = Article.objects.get(pk=pk)
    article = get_object_or_404(Article, pk=pk)
    # 수정하는 유저와, 게시글 작성 유저가 같은지 ?
    if request.user == article.user:
        if request.method == 'POST':
            form = ArticleForm(request.POST, instance=article)
            if form.is_valid():
                form.save()
                return redirect('articles:detail', article.pk)
        else:
            form = ArticleForm(instance=article)
    else:
        return redirect('articles:index')
    context = {
        'form': form,
        'article': article,
    }
    return render(request, 'articles/update.html', context)


# @require_POST
# def movie_review_delete(request, pk):
#     if request.user.is_authenticated:
#         # article = Article.objects.get(pk=pk)
#         article = get_object_or_404(Article, pk=pk)
#         if request.user == article.user:
#             article.delete()
#             return redirect('articles:index')
#     return redirect('articles:detail', article.pk)


# @require_POST
# def movie_review_comment_create(request, pk):
#     # article = Article.objects.get(pk=pk)
#     if request.user.is_authenticated:
#         article = get_object_or_404(Article, pk=pk)
#         comment_form = CommentForm(request.POST)
#         if comment_form.is_valid():
#             # Create, but don't save the new comment instance.
#             comment = comment_form.save(commit=False)
#             comment.article = article
#             comment.user = request.user
#             comment.save()
#             return redirect('articles:detail', article.pk)
#         context = {
#             'comment_form': comment_form,
#             'article': article,
#         }
#         return render(request, 'articles/detail.html', context)
#     return redirect('accounts:login')


# def movie_review_comment_update(request, movie_id, movie_review_id):
#     pass


# @require_POST
# def movie_review_comment_delete(request, article_pk, comment_pk):
#     # comment = Comment.objects.get(pk=comment_pk)
#     if request.user.is_authenticated:
#         comment = get_object_or_404(Comment, pk=comment_pk)
#         if request.user == comment.user:
#             comment.delete()
#     return redirect('articles:detail', article_pk)


# @require_POST
# def like(request, article_pk):
#     # 인증된 사용자만 가능
#     if request.user.is_authenticated:
#         article = get_object_or_404(Article, pk=article_pk)
#         # user가 article에 좋아요를 눌렀는지 안눌렀는지
        
#         # 1-1. user가 article을 좋아요 누른 전체유저에 포함이 되어있는지 안되어있는지.
#         # if request.user in article.like_users.all():
        
#         # 1-2. user가 article을 좋아요 누른 전체유저에 존재하는지.
#         if article.like_users.filter(pk=request.user.pk).exists():
#             # 좋아요 취소
#             article.like_users.remove(request.user)
#         else:
#             # 좋아요
#             article.like_users.add(request.user)
#         return redirect('articles:index')
#     return redirect('accounts:login')


@require_http_methods([])
def tmdb(request):
    # API_URL = 'https://api.themoviedb.org/3/movie/top_rated'

    # genres = [
    #     {
    #     "id": 28,
    #     "name": "액션"
    #     },
    #     {
    #     "id": 12,
    #     "name": "모험"
    #     },
    #     {
    #     "id": 16,
    #     "name": "애니메이션"
    #     },
    #     {
    #     "id": 35,
    #     "name": "코미디"
    #     },
    #     {
    #     "id": 80,
    #     "name": "범죄"
    #     },
    #     {
    #     "id": 99,
    #     "name": "다큐멘터리"
    #     },
    #     {
    #     "id": 18,
    #     "name": "드라마"
    #     },
    #     {
    #     "id": 10751,
    #     "name": "가족"
    #     },
    #     {
    #     "id": 14,
    #     "name": "판타지"
    #     },
    #     {
    #     "id": 36,
    #     "name": "역사"
    #     },
    #     {
    #     "id": 27,
    #     "name": "공포"
    #     },
    #     {
    #     "id": 10402,
    #     "name": "음악"
    #     },
    #     {
    #     "id": 9648,
    #     "name": "미스터리"
    #     },
    #     {
    #     "id": 10749,
    #     "name": "로맨스"
    #     },
    #     {
    #     "id": 878,
    #     "name": "SF"
    #     },
    #     {
    #     "id": 10770,
    #     "name": "TV 영화"
    #     },
    #     {
    #     "id": 53,
    #     "name": "스릴러"
    #     },
    #     {
    #     "id": 10752,
    #     "name": "전쟁"
    #     },
    #     {
    #     "id": 37,
    #     "name": "서부"
    #     }
    # ]

    # # Genre 생성
    # for genre in genres:
    #     genre_instance = Genre()
    #     genre_instance.id = genre['id']
    #     genre_instance.name = genre['name']
    #     genre_instance.save()

    # # TMDB API를 활용하여 1 ~ 21 페이지에 해당하는 영화 정보 추출
    # for page in range(1, 21):
    #     payload = {
    #         'api_key': '7571218b4ab42912852227b3b4ea629c',
    #         'language': 'ko-KR',
    #         'page': page,
    #         'region': 'KR',
    #     }
    #     response = requests.get(
    #         API_URL,
    #         params = payload,
    #     )
    #     # 20개의 영화 정보 생성
    #     movie_list = response.json().get('results')
        
    #     # movie_list(20개의 영화들)의 정보 중
    #     # movie(1개의 영화 정보)
    #     for movie in movie_list:
    #         # 영화 정보 가공
    #         if movie.get('backdrop_path'):
    #             movie['backdrop_path'] = 'https://image.tmdb.org/t/p/w500' + movie['backdrop_path']
    #         movie['poster_path'] = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']


    #         # Movie 생성
    #         movie_instance = Movie()

    #         movie_instance.id = movie['id']
    #         movie_instance.popularity = movie['popularity']
    #         movie_instance.video = movie['video']
    #         movie_instance.vote_count = movie['vote_count']
    #         movie_instance.vote_average = movie['vote_average']
    #         movie_instance.title = movie['title']
    #         movie_instance.release_date = movie['release_date']
    #         movie_instance.original_language = movie['original_language']
    #         movie_instance.original_title = movie['original_title']
    #         movie_instance.backdrop_path = movie['backdrop_path']
    #         movie_instance.adult = movie['adult']
    #         movie_instance.overview = movie['overview']
    #         movie_instance.poster_path =movie['poster_path']

    #         movie_instance.save()

    #         # 중계 테이블 생성 (M:N)
    #         for genre_id in movie['genre_ids']:
    #             genre_instance = get_object_or_404(Genre, id=genre_id)
    #             genre_instance.movies.add(movie_instance)


    return render(request, 'movies/data.html')