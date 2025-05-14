from flask import Flask, request, render_template, jsonify
import pickle
import joblib
import json
import os
from dotenv import load_dotenv
import requests

load_dotenv()
tmdb_key = os.getenv('TMDB_API_KEY')
if not tmdb_key:
    raise ValueError("TMDB_API_KEY not found in environment variables.")

app = Flask(__name__)

# Load data
movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = joblib.load('artifacts/similarity_compressed.pkl')

movie_list = movies['title'].values

# Recommendation logic
def recommend(movie):
    recommended_movies = []
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# Home route
@app.route('/')
def index():
    return render_template("index.html", movie_list=list(movie_list))

# CSS route
@app.route('/index.css')
def send_css():
    return app.send_static_file('index.css')

# JS route
@app.route('/autocomplete.js')
def send_js():
    return app.send_static_file('autocomplete.js')

# Recommendation endpoint
@app.route('/recommend')
def recommend_route():
    movie = request.args.get('movie')
    recommendations = recommend(movie)
    return jsonify(recommendations)

@app.route('/tmdb/<title>')
def get_tmdb_data(title):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': tmdb_key,
        'query': title
    }
    response = requests.get(url, params=params)
    return jsonify(response.json())

@app.route('/tmdb-genres')
def get_genres():
    import requests, os
    from flask import jsonify
    from dotenv import load_dotenv

    load_dotenv()
    tmdb_key = os.getenv("TMDB_API_KEY")
    
    url = f"https://api.themoviedb.org/3/genre/movie/list"
    params = {
        'api_key': tmdb_key,
        'language': 'en-US'
    }

    response = requests.get(url, params=params)

    try:
        data = response.json()
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': 'Failed to fetch genre data', 'details': str(e)}), 500


if __name__ == "__main__":
    # Tell Flask where to look for static files
    app.static_folder = 'static'
    app.run(debug=True)
