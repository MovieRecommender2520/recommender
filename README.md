# MovieRecommender
Recommender for movies based on preferences.

---

Dataset was preprocessed by turning keywords, genres, cast, crew, and overview (description) into one big tags column.  
It uses a counter vectorizer to combine the tags of each movie into a matrix where we use cosine similarity on the tags between movies.  
Movies with similar actors, director, genre, and keywords will be recommended.  

### How to run:  
1. Create virtual environment (venv):  
   `python3 -m venv .venv`
2. Activate virtual environment (venv):  
   `source .venv/bin/activate`
3. Install requirements:  
   `install pip install -r requirements.txt`
4. Run server on http://127.0.0.1:8080/:  
   `cd MovieRecommender`
   `python3 main.py`  


### Dataset:  
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata

Cleaned Dataset:  
![alt text](https://github.com/AriT000/MovieRecommender/blob/main/images/image-1.png)
