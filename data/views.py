from django.shortcuts import render
import requests

from .models import Movie, Genre


# def naver(request):
#     payload = {
#         'query': '인터스텔라',
#     }
#     headers = {
#         'X-Naver-Client-Id': '7ptwva7zZrZdP2xgQCb9',
#         'X-Naver-Client-Secret': '6EHPskOKjd',
#     }
#     response = requests.get(
#         'https://openapi.naver.com/v1/search/movie.json',
#         params = payload,
#         headers = headers,
#     )
#     response_dict = response.json()
#     pprint(response_dict)
#     context = {
#         'items': response_dict.get('items'),
#     }
#     return render(request, 'data/index.html', context)


# def kofic(request):
#     API_URL = 'http://www.kobis.or.kr/kobisopenapi/webservice/rest/movie/searchMovieList.json'
#     for i in range(1, 2):
#         payload = {
#             'key': 'a56b3a9ad2d444b6e20f9f1d8d00db28',
#             'curPage': i,
#             'itemPerPage': 100,
#             'prdtStartYear': '2000',
#             'prdtEndYear': '2020',
#         }
#         response = requests.get(
#             API_URL,
#             params = payload,
#         )
        
#         response_dict = response.json()
#         pprint(response_dict)
#         print(response.url)
#     return render(request, 'data/index.html')


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

    id2genre = {
        genre['id']: genre['name'] for genre in genres
    }
    # Genre 생성
    for genre_name in id2genre.values():
        genre_instance = Genre()
        genre_instance.name = genre_name
        genre_instance.save()

    genres = Genre.objects.all()
    for genre in genres:
        print(genre.name)

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
            movie['genre_names'] = [
                id2genre[genre_id] for genre_id in movie['genre_ids']
            ]

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
                if id2genre.get(genre_id):
                    genre_instance = Genre.objects.get(name=id2genre[genre_id])
                    genre_instance.movies.add(movie_instance)


    movies = Movie.objects.all()
    for movie in movies:
        print(movie.title)

    return render(request, 'data/index.html')