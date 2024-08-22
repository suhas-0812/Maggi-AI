import requests
import random
import time

# List of TMDb API Keys
tmdb_apis = ["66afc01f7ff932127dbf54cf04a46612", "23b938a50df0d1dbb6eba909a7baa47f", "8265bd1679663a7ea12ac168da84d2e8"]

def fetch_poster(movie_id, max_duration=15):
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > max_duration:
            return "Poster not found within the time limit"  # Return message if the loop exceeds 20 seconds

        TMDB_API_KEY = random.choice(tmdb_apis)  # Randomly select an API key
        url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key={TMDB_API_KEY}&language=en-US"
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check for HTTP errors
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                return full_path
        except requests.exceptions.RequestException:
            pass  # Suppress errors and continue trying
