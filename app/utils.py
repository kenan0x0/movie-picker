import os
import requests
import pickle

access_token = os.environ.get("ACCESS_TOKEN")

ENTRYPOINT_API_GENRE = "https://api.themoviedb.org/3/genre/movie/list"
ENTRYPOINT_API_MOVIE_POPULAR = "https://api.themoviedb.org/3/movie/popular"


# Important functions
# def get_popular_movies():
#     headers = {"Authorization":f"Bearer {access_token}"}

#     all_movies = []
    
#     for i in range(50):
#         params = {
#             "language":"en-US",
#             "page": i+1
#         }

#         movies = requests.get(url=ENTRYPOINT_API_MOVIE_POPULAR, headers=headers, params=params).json()["results"]
#         for movie in movies:
#             all_movies.append(movie)
    
#     with open('all_movies.pkl', 'wb') as f:
#         pickle.dump(all_movies, f)

#     return all_movies


def get_movie_details(id):
    ENDPOINT_API_MOVIE_DETAILS = f"https://api.themoviedb.org/3/movie/{id}"
    headers = {"Authorization":f"Bearer {access_token}"}

    return requests.get(url=ENDPOINT_API_MOVIE_DETAILS, headers=headers).json()


def get_movie_trailer(id):
    ENDPOINT_API_MOVIE_DETAILS = f"https://api.themoviedb.org/3/movie/{id}/videos"
    headers = {"Authorization":f"Bearer {access_token}"}

    return requests.get(url=ENDPOINT_API_MOVIE_DETAILS, headers=headers).json()["results"]


def get_movie_reviews(id):
    ENDPOINT_API_MOVIE_DETAILS = f"https://api.themoviedb.org/3/movie/{id}/reviews"
    headers = {"Authorization":f"Bearer {access_token}"}

    return requests.get(url=ENDPOINT_API_MOVIE_DETAILS, headers=headers).json()["results"]


def get_justwatch_movie_details(movie_name):
    ENDPOINT_JUSTWATCH_API = 'https://apis.justwatch.com/content/titles/en_NL/popular?language=en&body={"page_size":5,"page":1,"query":"' + movie_name + '","content_types":["movie"]}'
    movie_info = []
    try:
        req_movie_justwatch = requests.get(url=ENDPOINT_JUSTWATCH_API).json()["items"]
    except KeyError:
        return None
    for item in req_movie_justwatch:
        if movie_name == item["title"]:
            movie_info.append(item)
        else:
            pass
    
    if not movie_info:
        return None
    else:
        return movie_info[0]