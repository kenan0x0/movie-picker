from flask import Flask, url_for, redirect, render_template, request
import os
import random
from utils import (
    get_popular_movies,
    get_movie_details,
    get_movie_trailer,
    get_movie_reviews,
    get_justwatch_movie_details)

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = os.environ.get("SEC_KEY")
endpoint_poster = "https://www.themoviedb.org/t/p/w600_and_h900_bestv2"
endpoint_propic = "https://www.themoviedb.org/t/p/w150_and_h150_face"

# Note to self
# Provider IDS in JUSTWATCH
'''
8 is NETFLIX
10 && 119 are AMAZON PRIME VIDEO
71 is PATHE
'''
providers = [8, 10, 119, 72]

@app.route("/", methods=["POST", "GET"])
def landing_page():
    all_popular = get_popular_movies()

    initial_movie = random.choice(all_popular)
    movie = initial_movie["title"]
    img_url = f"{endpoint_poster}{initial_movie['poster_path']}"
    details = get_movie_details(initial_movie["id"])
    duration = details["runtime"]
    video_info = get_movie_trailer(initial_movie["id"])
    possible_videos = []
    for vid in video_info:
        possible_videos.append(vid)
    try:
        trailer_link = f"https://www.youtube.com/embed/{random.choice(possible_videos)['key']}"
    except IndexError:
        trailer_link = None
    reviews_info = get_movie_reviews(initial_movie["id"])
    reviews = []
    if len(reviews_info) > 0:
        for review in reviews_info:
            if review["author_details"]["avatar_path"] is None:
                reviews.append([review["author"], "https://i.stack.imgur.com/ZQT8Z.png", review["author_details"]["rating"], review["content"]])
            elif "gravatar" in review["author_details"]["avatar_path"]:
                reviews.append([review["author"], review["author_details"]["avatar_path"][1:], review["author_details"]["rating"], review["content"]])
            else:
                reviews.append([review["author"], f"{endpoint_propic}{review['author_details']['avatar_path']}", review["author_details"]["rating"], review["content"]])
    else:
        pass
    jw_movie_details = get_justwatch_movie_details(movie)
    try:
        release_year = jw_movie_details["original_release_year"]
    except TypeError:
        release_year = "No Release Year"
    offers = {}
    imdb_score = ""
    all_offers = jw_movie_details["offers"]
    for score in jw_movie_details["scoring"]:
        if "imdb:score" in score.values():
            imdb_score = score["value"]
    for offer in all_offers:
        if offer["provider_id"] in providers:
            if offer["provider_id"] == 8:
                offers["https://images.justwatch.com/icon/207360008/s100"] = offer["urls"]["standard_web"]
            elif offer["provider_id"] == 10 or offer["provider_id"] == 119:
                offers["https://www.justwatch.com/images/icon/52449861/s100"] = offer["urls"]["standard_web"]
            else:
                offers["https://www.justwatch.com/images/icon/899642/s100"] = offer["urls"]["standard_web"]
            
    

    if request.method == "POST":
        movies = get_popular_movies()
        rand_movie = random.choice(movies)
        movie = rand_movie["title"]
        img_url = f"{endpoint_poster}{rand_movie['poster_path']}"
        details = get_movie_details(rand_movie["id"])
        duration = details["runtime"]
        video_info = get_movie_trailer(rand_movie["id"])
        possible_videos = []
        for vid in video_info:
            possible_videos.append(vid)
        try:
            trailer_link = f"https://www.youtube.com/embed/{random.choice(possible_videos)['key']}"
        except:
            trailer_link = None
        reviews_info = get_movie_reviews(rand_movie["id"])
        reviews = []
        if len(reviews_info) > 0:
            for review in reviews_info:
                if review["author_details"]["avatar_path"] is None:
                    reviews.append([review["author"], "https://i.stack.imgur.com/ZQT8Z.png", review["author_details"]["rating"], review["content"]])
                elif "gravatar" in review["author_details"]["avatar_path"]:
                    reviews.append([review["author"], review["author_details"]["avatar_path"][1:], review["author_details"]["rating"], review["content"]])
                else:
                    reviews.append([review["author"], f"{endpoint_propic}{review['author_details']['avatar_path']}", review["author_details"]["rating"], review["content"]])
        else:
            pass
        jw_movie_details = get_justwatch_movie_details(movie)
        try:
            release_year = jw_movie_details["original_release_year"]
        except TypeError:
            release_year = "No Release Year"
        offers = {}
        imdb_score = ""
        all_offers = jw_movie_details["offers"]
        for score in jw_movie_details["scoring"]:
            if "imdb:score" in score.values():
                imdb_score = score["value"]
        all_offers = jw_movie_details["offers"]
        for offer in all_offers:
            if offer["provider_id"] in providers:
                if offer["provider_id"] == 8:
                    offers["https://images.justwatch.com/icon/207360008/s100"] = offer["urls"]["standard_web"]
                elif offer["provider_id"] == 10 or offer["provider_id"] == 119:
                    offers["https://www.justwatch.com/images/icon/52449861/s100"] = offer["urls"]["standard_web"]
                else:
                    offers["https://www.justwatch.com/images/icon/899642/s100"] = offer["urls"]["standard_web"]

    return render_template("home.html", movie=movie, img_url=img_url, duration=duration, trailer_link=trailer_link, reviews=reviews, offers=offers, release_year=release_year, imdb_score=imdb_score)


@app.errorhandler(404)
def resource_not_found(e):
    path = request.path
    return f"404, {path} not found!", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)