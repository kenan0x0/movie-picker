import streamlit as st
import pickle
import random
from helper_funcs import (
    get_movie_details,
    get_movie_trailer,
    get_movie_reviews,
    get_justwatch_movie_details,
    endpoint_poster,
    endpoint_propic
)

# Set the config of the page
st.set_page_config(
    page_title="Random Movie Picker",
    page_icon="platform/static/favicon.ico",
    layout="wide",
    initial_sidebar_state="auto"
    )

# Remove the watermark with CSS
with open("platform/static/main.css") as f:
    st.markdown('<style>{}</style>'.format(f.read()), unsafe_allow_html=True)



# Add page title
st.title("Random Movie Picker")

# $$$$$$$$$$ SIDEBAR AND POSSIBLE FILTERS $$$$$$$$$$
regen_button = st.sidebar.button(
    label="Generate Random Movie",
    help="Click to fetch and display a random movie",
    key="gen"
    )



# $$$$$$$$$$ MAIN PAGE $$$$$$$$$$


# Note to self
# Provider IDS in JUSTWATCH
providers = [8, 10, 119, 72, 2, 337, 35]


# Get all the popular movies
with open('platform/all_movies.pkl', 'rb') as f:
    all_popular = pickle.load(f)

# Select the initial movie to display
chosen_movie = random.choice(all_popular)

# Get the title of the initial movie
movie = chosen_movie["title"]

# Get the url of the movie's poster (poster is from themoviedb)
img_url = f"{endpoint_poster}{chosen_movie['poster_path']}"

# Get more deatils about the selected movie based on its id
details = get_movie_details(chosen_movie["id"])

# Get the duration of the movie in minutes
duration = details["runtime"]

# Get the release year
release_date = details["release_date"]
try:
    release_year = release_date[0:release_date.index("-")]
except ValueError:
    release_year = None

# Get the genres of the selected movie and add them to a list
genres = []
for genre in details["genres"]:
    genres.append(genre["name"])

# Get the available videos for the selected movie, add the videos to the list possible_videos
video_info = get_movie_trailer(chosen_movie["id"])
possible_videos = []
for vid in video_info:
    possible_videos.append(vid)

# Genreate the YouTube link of the video that will be displayed. If there were no videos then the trailer_url will be set to None
try:
    trailer_link = f"https://www.youtube.com/embed/{random.choice(possible_videos)['key']}"
except IndexError:
    trailer_link = None

# Get the reviews of the selected movie
reviews_info = get_movie_reviews(chosen_movie["id"])
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
if jw_movie_details is not None:
    imdb_score = ""
    for score in jw_movie_details["scoring"]:
        if "imdb:score" in score.values():
            imdb_score = str(score["value"])
            if len(imdb_score) == 1:
                imdb_score = f"{imdb_score}.0"
    try:
        all_offers = jw_movie_details["offers"]
        offers = {}
        for offer in all_offers:
            if offer["provider_id"] in providers:
                if offer["provider_id"] == 8:
                    offers["https://images.justwatch.com/icon/207360008/s100"] = offer["urls"]["standard_web"]
                elif offer["provider_id"] == 10 or offer["provider_id"] == 119:
                    offers["https://www.justwatch.com/images/icon/52449861/s100"] = offer["urls"]["standard_web"]
                elif offer["provider_id"] == 2:
                    offers["https://images.justwatch.com/icon/190848813/s100"] = offer["urls"]["standard_web"]
                elif offer["provider_id"] == 337:
                    offers["https://www.justwatch.com/images/icon/147638351/s100"] = offer["urls"]["standard_web"]
                elif offer["provider_id"] == 35:
                    offers["https://images.justwatch.com/icon/128599720/s100"] = offer["urls"]["standard_web"]
                else:
                    offers["https://www.justwatch.com/images/icon/899642/s100"] = offer["urls"]["standard_web"]
    except KeyError:
        offers = None
else:
    offers = None
    imdb_score = None