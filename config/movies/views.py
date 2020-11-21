from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods ,require_POST
from django.contrib.auth.decorators import login_required

from .models import Movie, Genre, Review, Comment, Oneline
from .forms import ReviewForm, CommentForm, OnelineForm

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


'''
영화 끝

################################################################

리뷰 시작
'''

def review_list(request, movie_id):
    # articles = Article.objects.prefetch_related('like_users').select_related('user').annotate(likes=Count('like_users')).order_by('-pk')
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    context = {
        'movie_id': movie_id,
        'reviews': reviews,
    }
    return render(request, 'movies/review/list.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def review_create(request, movie_id):
    if request.method == 'POST':
        form = ReviewForm(request.POST) 
        if form.is_valid():
            review = form.save(commit=False)
            movie = get_object_or_404(Movie, id=movie_id)
            review.user = request.user
            review.movie = movie
            # review.user = request.user
            review.save()
            return redirect('movies:review_detail', movie_id, review.id)
    else:
        form = ReviewForm()
    context = {
        'movie_id':movie_id,
        'form': form,
    }
    return render(request, 'movies/review/create.html', context)


def review_detail(request, movie_id, review_id):
    review = get_object_or_404(Review, id=review_id)
    comments = review.comments.all()
    comment_form = CommentForm()
    context = {
        'review': review,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'movies/review/detail.html', context)



@require_http_methods(['GET', 'POST'])
def review_update(request, movie_id, review_id):
    if request.user.is_authenticated:
        # 수정하는 유저와, 게시글 작성 유저가 같은지 ?
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            if request.method == 'POST':
                form = ReviewForm(request.POST, instance=review)
                if form.is_valid():
                    form.save()
                    return redirect('movies:review_detail', movie_id, review_id)
            else:
                form = ReviewForm(instance=review)
            context = {
                'review':review,
                'form': form,
            }
            return render(request, 'movies/review/update.html', context)
        return redirect('movies:review_detail', movie_id, review_id)
    return redirect('accounts:login')


@require_POST
def review_delete(request, movie_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            review.delete()
            return redirect('movies:review_list', movie_id)
    return redirect('accounts:login')

'''
리뷰 끝

################################################################

코멘트 시작
'''

@require_POST
def comment_create(request, movie_id, review_id):
    # article = Article.objects.get(pk=pk)
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id)
        comments = review.comments.all()
        comment_form = CommentForm(request.POST)
        if comment_form.is_valid():
            comment = comment_form.save(commit=False)
            comment.review = review
            comment.user = request.user
            comment.save()
            return redirect('movies:review_detail', movie_id, review_id)
        context = {
            'review': review,
            'comments': comments,
            'comment_form': comment_form,
        }
        return render(request, 'movies/review/detail.html', context)
    return redirect('accounts:login')


# def comment_update(request, movie_id, review_id, comment_id):
    # if request.user.is_authenticated:
    # review = get_object_or_404(Review, id=review_id)
    # comment_form = CommentForm(request.POST)
    # comments = review.comments.all()
    # if comment_form.is_valid():
    #     comment = comment_form.save(commit=False)
    #     comment.review = review
    #     # movie_comment.user = request.user
    #     comment.save()
    #     return redirect('movies:review_detail', movie_id, review_id)
    # context = {
    #     'review': review,
    #     'comments': comments,
    #     'comment_form': comment_form,
    # }
    # return render(request, 'movies/review/detail.html', context)


@require_POST
def comment_delete(request, movie_id, review_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
    return redirect('movies:review_detail', movie_id, review_id)

'''
코멘트 끝

################################################################

한줄평 시작
'''

@login_required
def oneline_list(request, movie_id):
    # articles = Article.objects.prefetch_related('like_users').select_related('user').annotate(likes=Count('like_users')).order_by('-pk')
    movie = get_object_or_404(Movie, id=movie_id)
    onelines = movie.onelines.all()
    context = {
        'movie_id': movie_id,
        'onelines': onelines,
    }
    return render(request, 'movies/oneline/list.html', context)


@login_required
@require_http_methods(['GET', 'POST'])
def onelinet_create(request, movie_id):
    if request.method == 'POST':
        movie = get_object_or_404(Movie, id=movie_id)
        form = OnelineForm(request.POST) 
        if form.is_valid():
            oneline = form.save(commit=False)
            movie = get_object_or_404(Movie, id=movie_id)
            oneline.user = request.user
            oneline.movie = movie
            oneline.save()
            return redirect('movies:oneline_list', movie_id)
    else:
        form = OnelineForm()
    context = {
        'form': form,
        'movie_id':movie_id,
    }
    return render(request, 'movies/oneline/create.html', context)


# # @login_required
# @require_http_methods(['GET', 'POST'])
# def oneline_update(request, movie_id, oneline_id):
#     # 수정하는 유저와, 게시글 작성 유저가 같은지 ?
#     # if request.user == article.user:
#     oneline = get_object_or_404(Oneline, id=oneline_id)
#     if request.method == 'POST':
#         form = OnelineForm(request.POST, instance=oneline)
#         if form.is_valid():
#             form.save()
#             return redirect('movies:oneline_list', movie_id, oneline_id)
#     else:
#         form = OnelineForm(instance=oneline)
#     # else:
#     #     return redirect('articles:index')
#     context = {
#         'form': form,
#     }
#     return render(request, 'movies/oneline/update.html', context)


@require_POST
def oneline_delete(request, movie_id, oneline_id):
    if request.user.is_authenticated:
        oneline = get_object_or_404(Oneline, id=oneline_id)
        if request.user == oneline.user:
            oneline.delete()
            return redirect('movies:oneline_list', movie_id)
    return redirect('accounts:login')

'''
한줄평 끝

################################################################

좋아요 시작
'''

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

'''
좋아요 끝

################################################################

추천 알고리즘 시작
'''
# from django.db.models import Q      


# host = 'https://api.openweathermap.org'
# path = '/data/2.5/onecall'
# params = {
#     'lat': '35.1595454',
#     'lon': '126.8526012',
#     'appid': 'fb274443560bf75e3801324989c0959e',
#     'lang': 'kr',
# }
# url = host + path


# @require_GET
# def recommended(request):
#     # api 요청
#     response = requests.get(url, params=params)
#     data = response.json()
#     weather_id = str(data["current"]["weather"][0]["id"])
#     temp = data["current"]["temp"] - 273.15
    
#     if weather_id[0] == '2':
#         genre = ['53', '27', '9648']
#         weather_id = '천둥치는'
#     elif weather_id[0] == '3':
#         genre = ['10749', '18', '10402']
#         weather_id = '이슬비 내리는'
#     elif weather_id[0] == '5':
#         genre = ['53', '10770', '99']
#         weather_id = '비오는 '
#     elif weather_id[0] == '6':
#         genre = ['10749', '18', '35']
#         weather_id = '소복소복 눈내리는'
#     elif weather_id[0] == '7':
#         genre = ['12', '9648', '14']
#         weather_id = '먼지날리는'
#     elif weather_id[0] == '8':
#         # 맑은날씨
#         if weather_id[2] == '0':
#             if temp <= 0:
#                 genre = ['99', '80', '37']
#             elif 0 < temp <= 15:
#                 genre = ['35', '36', '10402']
#             else:
#                 genre = ['53', '27', '9648']
#             weather_id = '구름한점 없이 맑은'
#         # 흐린날씨
#         else:
#             if temp <= 0:
#                 genre = ['10770', '12', '10402']
#             elif 0 < temp <= 15:
#                 genre = ['10752', '99', '36']
#             else:
#                 genre = ['14', '28', '878']  
#             weather_id = '구름이 많은'
    

#     # 조건문에 따른 필터링 (id, temp를 활용)

#     movies = Movie.objects.filter(Q(genres=genre[0]) | Q(genres=genre[1]) | Q(genres=genre[2]))
#     context = {
#         'movies': movies,
#         'weather_id': weather_id,
#         'temp': temp
#     }
#     return render(request, 'movies/recommended.html', context)


'''
추천 알고리즘 끝

################################################################

데이터 시작
'''

@require_http_methods(['GET'])
def tmdb(request):
    API_URL = 'https://api.themoviedb.org/3/movie/top_rated'

    genres = [
        {
        "id": 28,
        "name": "액션"
        },
        {
        "id": 12,
        "name": "모험"
        },
        {
        "id": 16,
        "name": "애니메이션"
        },
        {
        "id": 35,
        "name": "코미디"
        },
        {
        "id": 80,
        "name": "범죄"
        },
        {
        "id": 99,
        "name": "다큐멘터리"
        },
        {
        "id": 18,
        "name": "드라마"
        },
        {
        "id": 10751,
        "name": "가족"
        },
        {
        "id": 14,
        "name": "판타지"
        },
        {
        "id": 36,
        "name": "역사"
        },
        {
        "id": 27,
        "name": "공포"
        },
        {
        "id": 10402,
        "name": "음악"
        },
        {
        "id": 9648,
        "name": "미스터리"
        },
        {
        "id": 10749,
        "name": "로맨스"
        },
        {
        "id": 878,
        "name": "SF"
        },
        {
        "id": 10770,
        "name": "TV 영화"
        },
        {
        "id": 53,
        "name": "스릴러"
        },
        {
        "id": 10752,
        "name": "전쟁"
        },
        {
        "id": 37,
        "name": "서부"
        }
    ]

    # Genre 생성
    for genre in genres:
        genre_instance = Genre()
        genre_instance.id = genre['id']
        genre_instance.name = genre['name']
        genre_instance.save()

    # TMDB API를 활용하여 1 ~ 21 페이지에 해당하는 영화 정보 추출
    for page in range(1, 21):
        payload = {
            'api_key': '7571218b4ab42912852227b3b4ea629c',
            'language': 'ko-KR',
            'page': page,
            'region': 'KR',
        }
        response = requests.get(
            API_URL,
            params = payload,
        )
        # 20개의 영화 정보 생성
        movie_list = response.json().get('results')
        
        # movie_list(20개의 영화들)의 정보 중
        # movie(1개의 영화 정보)
        for movie in movie_list:
            # 영화 정보 가공
            if movie.get('backdrop_path'):
                movie['backdrop_path'] = 'https://image.tmdb.org/t/p/w500' + movie['backdrop_path']
            movie['poster_path'] = 'https://image.tmdb.org/t/p/w500' + movie['poster_path']


            # Movie 생성
            movie_instance = Movie()

            movie_instance.id = movie['id']
            movie_instance.popularity = movie['popularity']
            movie_instance.video = movie['video']
            movie_instance.vote_count = movie['vote_count']
            movie_instance.vote_average = movie['vote_average']
            movie_instance.title = movie['title']
            movie_instance.release_date = movie['release_date']
            movie_instance.original_language = movie['original_language']
            movie_instance.original_title = movie['original_title']
            movie_instance.backdrop_path = movie['backdrop_path']
            movie_instance.adult = movie['adult']
            movie_instance.overview = movie['overview']
            movie_instance.poster_path =movie['poster_path']

            movie_instance.save()

            # 중계 테이블 생성 (M:N)
            for genre_id in movie['genre_ids']:
                genre_instance = get_object_or_404(Genre, id=genre_id)
                genre_instance.movies.add(movie_instance)


    return render(request, 'movies/data.html')