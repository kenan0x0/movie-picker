from flask import Flask, url_for, redirect, render_template, request
import requests

access_token = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI2M2ZmODQzODlkZDJhMzUzYTFlODg4NDUyNGYxYzM0YSIsInN1YiI6IjYxNTBiNGUzMmQ4ZWYzMDA4YjE0MzYzYyIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.4dCWoKqGO8SBspauOrrqP9CwSsN5howdCqbxoUu3jHc"

ENTRYPOINT_API_GENRE = f"https://api.themoviedb.org/3/genre/movie/list"
ENTRYPOINT_API_MOVIE_POPULAR = f"https://api.themoviedb.org/3/movie/popular"

app = Flask(__name__)

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


@app.route("/", methods=["GET", "POST"])
def index():
    movie = ""
    if request.method == "POST":
        movie = get_popular_movies()[0][0]["original_title"]
        
    return render_template("home.html", movie=movie)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)