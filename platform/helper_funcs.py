import os
import requests
import pickle


'''
8 is NETFLIX
10 && 119 are AMAZON PRIME VIDEO
71 is PATHE
2 is APPLE'S ITUNES
337 is DINSEY
35 is RAKUTEN
'''


access_token = os.environ.get("ACCESS_TOKEN")


endpoint_poster = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
endpoint_propic = "https://www.themoviedb.org/t/p/w150_and_h150_face"


ENTRYPOINT_API_GENRE = "https://api.themoviedb.org/3/genre/movie/list"
ENTRYPOINT_API_MOVIE_POPULAR = "https://api.themoviedb.org/3/movie/popular"


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