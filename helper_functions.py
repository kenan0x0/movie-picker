import requests
import pickle
import os

TMDB_ENTRYPOINT = "https://api.themoviedb.org/3"
tmdb_access_token = os.environ.get("ACCESS_TOKEN")

def get_all_popular():
    all_movies_ids = []
    headers = {"Authorization":f"Bearer {tmdb_access_token}"}
    for i in range(100):
        params = {
            "language":"en-US",
            "page": i+1
        }
        req_all_popular = requests.get(url=f"{TMDB_ENTRYPOINT}/movie/popular", headers=headers, params=params).json()["results"]
        for movie in req_all_popular:
            all_movies_ids.append(movie["id"])
    return all_movies_ids

def get_imdb_ids(list_ids):
    headers = {"Authorization":f"Bearer {tmdb_access_token}"}
    imdb_ids = []
    for movie_id in list_ids:
        req_movie_details = requests.get(url=f"{TMDB_ENTRYPOINT}/movie/{movie_id}", headers=headers).json()
        imdb_ids.append([req_movie_details["original_title"], req_movie_details["imdb_id"]])

    return imdb_ids

all_tmdb_ids = get_all_popular()
all_imdb_ids = get_imdb_ids(all_tmdb_ids)


with open('all_movies_imdb.pkl', 'wb') as f:
        pickle.dump(all_imdb_ids, f)