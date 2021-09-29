from flask import Flask, url_for, redirect, render_template, request
import os
from utils import get_all_genres, get_popular_movies

app = Flask(__name__)
app.debug = True
app.config["SECRET_KEY"] = os.environ.get("SEC_KEY")

@app.route("/", methods=["POST", "GET"])
def landing_page():
    genres = get_all_genres()
    movie = ""
    if request.method == "POST":
        movie = get_popular_movies()[0][0]["original_title"]
        
    return render_template("home.html", geres=genres, movie=movie)

@app.errorhandler(404)
def resource_not_found(e):
    path = request.path
    return f"404, {path} not found!", 404

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)