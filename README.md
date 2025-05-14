# Recommender

This is a web-based movie recommender system that suggests similar movies based on a combination of overview, genres, keywords, cast, and crew information. The application includes a modern user interface with live search functionality and integration with the TMDB API for enriched metadata and posters.

## Features

- Autocomplete search with keyboard navigation
- Movie poster display using TMDB API
- Genre badges under each recommended movie
- Client-side caching of API results for faster repeat searches

## How to Run

1. Create a virtual environment:
   ```bash
   python3 -m venv .venv
   ```

2. Activate the virtual environment:
   ```bash
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Add your TMDB API key to a `.env` file:
   ```env
   TMDB_API_KEY=your_api_key_here
   ```

5. Run the Flask server:
   ```bash
   python app.py
   ```

6. Open your browser at:
   ```
   http://127.0.0.1:5000
   ```

## Dataset

The application uses the TMDB 5000 movie dataset from Kaggle. The data is preprocessed to create a unified `tags` column combining overview, genres, keywords, cast, and crew, which is vectorized and used for cosine similarity.

Dataset source:  
https://www.kaggle.com/datasets/tmdb/tmdb-movie-metadata
