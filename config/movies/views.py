from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods ,require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q      
from django.http.response import JsonResponse

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status

from .models import Movie, Genre, Review, Comment, Oneline
from .forms import ReviewForm, CommentForm, OnelineForm
from .serializers import ReviewSerializer, CommentSerializer, OnelineSerializer

import requests

from datetime import datetime



'''
추천 알고리즘 시작

################################################################
'''


today = ''
weather_movies = set()


def weather_recommand_genre_id_list():
    # api 요청
    params = {
        'lat': '35.1595454',
        'lon': '126.8526012',
        'appid': 'fb274443560bf75e3801324989c0959e',
        'lang': 'kr',
    }
    url = 'https://api.openweathermap.org/data/2.5/onecall'
    response = requests.get(url, params=params)
    data = response.json()
    weather_id = str(data["current"]["weather"][0]["id"])
    temp = data["current"]["temp"] - 273.15
    
    if weather_id[0] == '2':
        genres = [80, 27, 53, 9648,]
        # weather_id = '천둥치는'
    elif weather_id[0] == '3':
        genres = [80, 27, 53, 9648,]
        # weather_id = '이슬비 내리는'
    elif weather_id[0] == '5':
        genres = [80, 27, 53, 9648,]
        # weather_id = '비오는 '
    elif weather_id[0] == '6':
        genres = [10751, 18, 10770,]
        # weather_id = '소복소복 눈내리는'
    elif weather_id[0] == '7':
        genres = [37, 10752, 878, 36, 99]
        # weather_id = '먼지날리는'
    elif weather_id[0] == '8':
        # 맑은날씨
        if weather_id[2] == '0':
            if temp <= 0:
                genres = [28, 12, 35, 14, 10402, 10749]
            elif 0 < temp <= 15:
                genres = [28, 12, 35, 14, 10402, 10749]
            else:
                genres = [28, 12, 35, 14, 10402, 10749]
            # weather_id = '구름한점 없이 맑은'
        # 흐린날씨
        else:
            if temp <= 0:
                genres = [80, 27, 53, 9648,]
            elif 0 < temp <= 15:
                genres = [80, 27, 53, 9648,]
            else:
                genres = [80, 27, 53, 9648,]  
            # weather_id = '구름이 많은'
    return genres


'''
추천 알고리즘 끝

################################################################

영화 시작
'''


@login_required
@require_http_methods(['GET'])
def index(request):
    movies = Movie.objects.all()
    genres = Genre.objects.all()

    global today, weather_movies
    if today != datetime.today().strftime("%Y%m%d") or (not weather_movies and genres):
        today = datetime.today().strftime("%Y%m%d")
        for genre_id in weather_recommand_genre_id_list():
            weather_movies.update(set(get_object_or_404(Genre, id=genre_id).movies.all()))


    context = {
        'weather_movies': list(weather_movies),
        'movies': movies,
        'genres': genres,
    }
    return render(request, 'movies/index.html', context)


@login_required
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

@login_required
def review_list(request, movie_id):
    # articles = Article.objects.prefetch_related('like_users').select_related('user').annotate(likes=Count('like_users')).order_by('-pk')
    movie = get_object_or_404(Movie, id=movie_id)
    reviews = movie.reviews.all()
    form = ReviewForm()
    context = {
        'movie': movie,
        'reviews': reviews,
        'form': form,
    }
    return render(request, 'movies/review/list.html', context)


@api_view(['POST'])
def review_create(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = ReviewSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            return Response({ 'data' : 'success!' })
    return redirect('accounts:login')


@login_required
def review_detail(request, movie_id, review_id):
    movie = get_object_or_404(Movie, id=movie_id)
    review = get_object_or_404(Review, id=review_id)
    review_form = ReviewForm(instance=review)
    comments = review.comments.all()
    comment_form = CommentForm()
    context = {
        'movie': movie,
        'review': review,
        'review_form': review_form,
        'comments': comments,
        'comment_form': comment_form,
    }
    return render(request, 'movies/review/detail.html', context)



@api_view(['POST'])
def review_update(request, movie_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            movie = get_object_or_404(Movie, id=movie_id)
            serializer = ReviewSerializer(data=request.data, instance=review)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, movie=movie)
                return Response({ 'data' : 'success!' })


@require_POST
def review_delete(request, movie_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id)
        if request.user == review.user:
            review.delete()
            return redirect('movies:review_list', movie_id)

'''
리뷰 끝

################################################################

코멘트 시작
'''

@api_view(['POST'])
def comment_create(request, movie_id, review_id):
    if request.user.is_authenticated:
        review = get_object_or_404(Review, id=review_id)
        serializer = CommentSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            comment = serializer.save(user=request.user, review=review)
            return Response({'commentId': comment.id})


@api_view(['POST'])
def comment_update(request, movie_id, review_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            review = get_object_or_404(Review, id=review_id)
            serializer = CommentSerializer(data=request.data, instance=comment)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, review=review)
                return Response({'commentId': comment.id})


@api_view(['POST'])
def comment_delete(request, movie_id, review_id, comment_id):
    if request.user.is_authenticated:
        comment = get_object_or_404(Comment, id=comment_id)
        if request.user == comment.user:
            comment.delete()
            return Response({'commentId': comment.id})


'''
코멘트 끝

################################################################

한줄평 시작
'''

@login_required
def oneline_list(request, movie_id):
    # articles = Article.objects.prefetch_related('like_users').select_related('user').annotate(likes=Count('like_users')).order_by('-pk')
    form = OnelineForm()
    movie = get_object_or_404(Movie, id=movie_id)
    onelines = movie.onelines.all()
    context = {
        'movie': movie,
        'onelines': onelines,
        'form':form,
    }
    return render(request, 'movies/oneline/list.html', context)



@api_view(['POST'])
def oneline_create(request, movie_id):
    if request.user.is_authenticated:
        movie = get_object_or_404(Movie, id=movie_id)
        serializer = OnelineSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(user=request.user, movie=movie)
            
            vote_average = movie.vote_average
            vote_count = movie.vote_count

            vote_average = (vote_average * vote_count + serializer.data.get('vote_rating', 0)) / (vote_count + 1)
            vote_count += 1
            Movie.objects.filter(id=movie_id).update(vote_average=vote_average, vote_count=vote_count)

            return Response({ 'data' : 'success!' })


@api_view(['POST'])
def oneline_update(request, movie_id, oneline_id):
    if request.user.is_authenticated:
        oneline = get_object_or_404(Oneline, id=oneline_id)
        if request.user == oneline.user:
            movie = get_object_or_404(Movie, id=movie_id)
            serializer = OnelineSerializer(data=request.data, instance=oneline)
            if serializer.is_valid(raise_exception=True):
                serializer.save(user=request.user, movie=movie)
                return Response({ 'data' : 'success!' })


@require_POST
def oneline_delete(request, movie_id, oneline_id):
    if request.user.is_authenticated:
        oneline = get_object_or_404(Oneline, id=oneline_id)
        if request.user == oneline.user:
            oneline.delete()
        return redirect('movies:oneline_list', movie_id)


'''
한줄평 끝

################################################################

좋아요 시작
'''


@api_view(['POST'])
def review_like(request, movie_id, review_id):
    if request.user.is_authenticated:
        like_status = request.data.get('like_status')
        user = request.user
        review = get_object_or_404(Review, id=review_id)
        if like_status:
            if review.like_users.filter(id=user.id).exists():
                review.like_users.remove(user)
                like_status = None
            else:
                review.like_users.add(user)
                if review.dislike_users.filter(id=user.id).exists():
                    review.dislike_users.remove(user)
        else:
            if review.dislike_users.filter(id=user.id).exists():
                review.dislike_users.remove(user)
                like_status = None
            else:
                review.dislike_users.add(user)
                if review.like_users.filter(id=user.id).exists():
                    review.like_users.remove(user)
        
        data = {
            'like_status':like_status,
            'like_count':review.like_users.count(),
            'dislike_count':review.dislike_users.count()
        }
        return JsonResponse(data)



@api_view(['POST'])
def oneline_like(request, movie_id, oneline_id):
    if request.user.is_authenticated:
        like_status = request.data.get('like_status')
        user = request.user
        oneline = get_object_or_404(Oneline, id=oneline_id)
        if like_status:
            if oneline.like_users.filter(id=user.id).exists():
                oneline.like_users.remove(user)
                like_status = None
            else:
                oneline.like_users.add(user)
                if oneline.dislike_users.filter(id=user.id).exists():
                    oneline.dislike_users.remove(user)
        else:
            if oneline.dislike_users.filter(id=user.id).exists():
                oneline.dislike_users.remove(user)
                like_status = None
            else:
                oneline.dislike_users.add(user)
                if oneline.like_users.filter(id=user.id).exists():
                    oneline.like_users.remove(user)
        
        data = {
            'like_status':like_status,
            'like_count':oneline.like_users.count(),
            'dislike_count':oneline.dislike_users.count()
        }
        return JsonResponse(data)




'''
좋아요 끝

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
    for page in range(1, 51):
        payload = {
            'api_key': 'my-key',
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


    # 날씨별 영화추천 초기화
    global today, weather_movies
    today = datetime.today().strftime("%Y%m%d")
    for genre_id in weather_recommand_genre_id_list():
        weather_movies.update(set(get_object_or_404(Genre, id=genre_id).movies.all()))

    return redirect('accounts:signup')
