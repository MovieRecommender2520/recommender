from bottle import Bottle, run, route, request, template, static_file
import pickle
import json
import joblib

movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
similarity = joblib.load('artifacts/similarity_compressed.pkl')

movie_list = movies['title'].values

def recommend(movie):
    recommended_movies = []
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])
    for i in distances[1:6]:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

@route('/')
def index():
    return template("index.html", movie_list=json.dumps(list(movie_list)))

@route('/index.css')
def send_css():
    return static_file('index.css', root='./static')

@route('/autocomplete.js')
def send_js():
    return static_file('autocomplete.js', root='./static')

@route('/recommend')
def recommend_route():
    movie = request.query.movie
    recommendations = recommend(movie)
    return json.dumps(recommendations)

run(host="localhost", port=8080)