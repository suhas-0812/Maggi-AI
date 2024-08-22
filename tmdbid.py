import requests
import random
import time

# List of TMDb API Keys
tmdb_apis = ["66afc01f7ff932127dbf54cf04a46612", "23b938a50df0d1dbb6eba909a7baa47f", "8265bd1679663a7ea12ac168da84d2e8"]

# TMDb API URL
TMDB_SEARCH_URL = "https://api.themoviedb.org/3/search/movie"

def fetch_tmdb_movie_id(title, release_year=None, original_language=None, max_duration=15):
    start_time = time.time()
    
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > max_duration:
            return "Not found"  # Return 0 if the search exceeds 10 minutes
        
        TMDB_API_KEY = random.choice(tmdb_apis)  # Randomly select an API key
        params = {
            "api_key": TMDB_API_KEY,
            "query": title,
            "primary_release_year": release_year,  # Ensure the release year matches
            "region": "IN",
            "original_language": original_language  # Use original_language instead of language
        }
        try:
            response = requests.get(TMDB_SEARCH_URL, params=params)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            if data['results']:
                # Search through all results to find the best match
                for movie in data['results']:
                    if movie['title'].lower() == title.lower() and movie['release_date'][:4] == str(release_year):
                        return movie['id']
        except requests.exceptions.RequestException:
            pass  # Suppress any errors and continue trying


