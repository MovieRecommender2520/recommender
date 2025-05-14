from flask import Blueprint, request, render_template, jsonify
import pickle
import joblib
import os
import requests
from dotenv import load_dotenv

routes_bp = Blueprint('routes', __name__)

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

load_dotenv()
tmdb_key = os.getenv('TMDB_API_KEY')
if not tmdb_key:
    raise ValueError("TMDB_API_KEY not found in environment variables.")

# Home route
@routes_bp.route('/')
def index():
    return render_template("index.html", movie_list=list(movie_list))

# CSS route
@routes_bp.route('/index.css')
def send_css():
    return routes_bp.send_static_file('index.css')

# JS route
@routes_bp.route('/autocomplete.js')
def send_js():
    return routes_bp.send_static_file('autocomplete.js')

# Recommendation endpoint
@routes_bp.route('/recommend')
def recommend_route():
    movie = request.args.get('movie')
    recommendations = recommend(movie)
    return jsonify(recommendations)

@routes_bp.route('/tmdb/<title>')
def get_tmdb_data(title):
    url = f"https://api.themoviedb.org/3/search/movie"
    params = {
        'api_key': tmdb_key,
        'query': title
    }
    response = requests.get(url, params=params)
    return jsonify(response.json())

@routes_bp.route('/tmdb-genres')
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
