import numpy as np
import pandas as pd
import os
import ast

movies = pd.read_csv('data/tmdb_5000_movies.csv')
credits = pd.read_csv('data/tmdb_5000_credits.csv')

# merge columns
movies = movies.merge(credits, on = "title")
# drop budget, homepage, id, original_language, original_title, popularity, production_companies, 
# production_countries, release_date, revenue, runtime, spoken languages, status, tagline, vote_average, and vote_count
movies = movies[['movie_id','title','overview','genres','keywords','cast','crew']]
movies.dropna(inplace=True)

# convert columns to list
def convert(text):
    list = []
    for i in ast.literal_eval(text):
        list.append(i['name'])
    return list

# apply convert to genre and keywords columns
movies['genres'] = movies['genres'].apply(convert)
movies['keywords'] = movies['keywords'].apply(convert)

# convert cast to first 5 cast members (most important/well known)
def convert_cast(text):
    list = []
    counter = 0
    for i in ast.literal_eval(text):
        if counter < 5:
            list.append(i['name'])
        counter += 1
    return list

# apply convert_cast 
movies['cast'] = movies['cast'].apply(convert_cast)

# convert crew to just director
def convert_crew(text):
    list = []
    for i in ast.literal_eval(text):
        if i['job'] == 'Director':
            list.append(i['name'])
            break
    return list

# apply convert_crew to crew column
movies['crew'] = movies['crew'].apply(convert_crew)

# convert overview to list to concatenate overview + genre + keywords + cast + crew
movies['overview'] = movies['overview'].apply(lambda x:x.split())

# Remove spaces for values with more than 1 word
# ie. Sam Worthington must be SamWorthington to not be
# confused with Sam Mendes (each first and last name
# will be considered as separate words. We must fix this)
def remove_space(word):
    list = []
    for i in word:
        list.append(i.replace(" ", ""))
    return list
# apply remove_space to these columns
movies['cast'] = movies['cast'].apply(remove_space)
movies['crew'] = movies['crew'].apply(remove_space)
movies['genres'] = movies['genres'].apply(remove_space)
movies['keywords'] = movies['keywords'].apply(remove_space)


# concatenate overview + genre + keywords + cast + crew
# into a generalized 'tags' column
movies['tags'] = movies['overview'] + movies['genres'] + movies['keywords'] + movies['cast'] + movies['crew']

# now drop the columns that were mixed into the tags column
new_df = movies[['movie_id','title','tags']]

# convert tags from list to stringg
new_df['tags'] = new_df['tags'].apply(lambda x: " ".join(x))

# Convert tags to lowercase
new_df['tags'] = new_df['tags'].apply(lambda x:x.lower())

# export cleaned dataset to csv
new_df.to_csv('cleaned_data.csv', index=False)

import nltk
from nltk.stem import PorterStemmer
ps = PorterStemmer()

# We use this to make words like love and loved and loving to be just "lov"
# This is to help romance movies with love in their description to be deemed "similar"
def stems(text):
    list = []
    for i in text.split():
        list.append(ps.stem(i))
    return " ".join(list)

# apply stems to tags column
new_df['tags'] = new_df['tags'].apply(stems)

# implementing counter vectorizer but also getting rid of useless words
# like "in", "the", "a", etc...
from sklearn.feature_extraction.text import CountVectorizer
cv = CountVectorizer(max_features=5000, stop_words= 'english')

# vectorizing tags column
vector = cv.fit_transform(new_df['tags']).toarray()

from sklearn.metrics.pairwise import cosine_similarity
# using cosine similarity 
# store results of running cosine similarity on tags vector
similarity = cosine_similarity(vector)

# the actual recommend movie that recommends 5 other movies
def recommend(movie):
    index = new_df[new_df['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key = lambda x: x[1])
    for i in distances[1:6]:
        print(new_df.iloc[i[0]].title)

# dump the dataframe and model into artifacts
os.makedirs('artifacts', exist_ok=True)
import pickle
pickle.dump(new_df, open('artifacts/movie_list.pkl', 'wb'))
pickle.dump(similarity, open('artifacts/similarity.pkl', 'wb'))