import os
import requests
import pickle

ENTRYPOINT_API_MOVIE_POPULAR = "https://api.themoviedb.org/3/movie/popular"

# Max is 500 pages for future reference

# Important functions
def get_popular_movies():
    headers = {"Authorization":f"Bearer {os.environ.get('ACCESS_TOKEN')}"}

    all_movies = []
    
    for i in range(50):
        params = {
            "language":"en-US",
            "page": i+1
        }

        movies = requests.get(url=ENTRYPOINT_API_MOVIE_POPULAR, headers=headers, params=params).json()["results"]
        for movie in movies:
            all_movies.append(movie)
    
    with open('all_movies.pkl', 'wb') as f:
        pickle.dump(all_movies, f)

    return all_movies

get_popular_movies()