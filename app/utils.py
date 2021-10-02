import os
import requests

access_token = os.environ.get("ACCESS_TOKEN")

ENTRYPOINT_API_GENRE = "https://api.themoviedb.org/3/genre/movie/list"
ENTRYPOINT_API_MOVIE_POPULAR = "https://api.themoviedb.org/3/movie/popular"


# Important functions
def get_popular_movies():
    headers = {"Authorization":f"Bearer {access_token}"}

    all_movies = []
    
    for i in range(20):
        params = {
            "language":"en-US",
            "page": i+1
        }

        movies = requests.get(url=ENTRYPOINT_API_MOVIE_POPULAR, headers=headers, params=params).json()["results"]
        for movie in movies:
            all_movies.append(movie)

    return all_movies



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


# Function that gets all movie genres with their ids
# def get_all_genres():
#     headers = {"Authorization":f"Bearer {access_token}"}
#     params = {
#         "language":"en-US",
#     }

#     genres = requests.get(url=ENTRYPOINT_API_GENRE, headers=headers, params=params).json()["genres"]
    
#     return genres