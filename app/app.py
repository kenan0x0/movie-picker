from flask import Flask, url_for, redirect, render_template, request
import os
import random
from utils import get_popular_movies, get_movie_details

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = os.environ.get("SEC_KEY")
endpoint_poster = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"

@app.route("/", methods=["POST", "GET"])
def landing_page():
    all_popular = get_popular_movies()

    initial_movie = random.choice(all_popular)
    movie = initial_movie["title"]
    img_url = f"{endpoint_poster}{initial_movie['poster_path']}"

    if request.method == "POST":
        movies = get_popular_movies()
        rand_movie = random.choice(movies)
        movie = rand_movie["title"]
        img_url = f"{endpoint_poster}{rand_movie['poster_path']}"
        details = get_movie_details(rand_movie["id"])
        # print(movies)

    return render_template("home.html", movie=movie, img_url=img_url)


@app.errorhandler(404)
def resource_not_found(e):
    path = request.path
    return f"404, {path} not found!", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)