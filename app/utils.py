import os
import requests

access_token = os.environ.get("ACCESS_TOKEN")

ENTRYPOINT_API_GENRE = f"https://api.themoviedb.org/3/genre/movie/list"
ENTRYPOINT_API_MOVIE_POPULAR = f"https://api.themoviedb.org/3/movie/popular"


# Important functions
def get_popular_movies():
    headers = {"Authorization":f"Bearer {access_token}"}

    all_movies = []
    
    for i in range(3):
        params = {
            "language":"en-US",
            "page": i+1
        }

        movies = requests.get(url=ENTRYPOINT_API_MOVIE_POPULAR, headers=headers, params=params).json()["results"]
        all_movies.append(movies)

    return all_movies


# Function that gets all movie genres with their ids
def get_all_genres():
    headers = {"Authorization":f"Bearer {access_token}"}
    params = {
        "language":"en-US",
    }

    genres = requests.get(url=ENTRYPOINT_API_GENRE, headers=headers, params=params).json()["genres"]
    
    return genres