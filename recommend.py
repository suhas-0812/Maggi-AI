import google.generativeai as genai
import json

# Configure Google Generative AI
GOOGLE_API_KEY = "AIzaSyBGLiHCH_XM2NJOYT5GV6jaclzF5CW6EEM"
genai.configure(api_key=GOOGLE_API_KEY)

# Initialize the generative model
model_text = genai.GenerativeModel("gemini-1.5-pro-latest")

def generate_movie_recommendation_prompt(user_input):
    # Define the prompt with all details
    prompt = """
    Description: Develop an AI-driven tool to recommend movies based on user preferences for genres, mood, language, movie length, release year, and specific cast or director. The tool should fetch movies preferably from TMDb, ensuring accurate and existing movie details without any hallucinations.

    Functionality:

    Recommendation:
    Recommend three movies based on the provided user inputs: genres, mood, language, movie length (in range format), release year (in range format), and specific cast or director.
    If all input fields are empty, recommend three random movies with good ratings and popularity.

    Input:
    Genres (e.g., Action, Comedy, Drama)
    Mood (e.g., Happy, Sad, Exciting)
    Language (e.g., English, Hindi, Spanish)
    Movie Length (in range format, e.g., 90-120 minutes)
    Release Year (in range format, e.g., 2000-2020)
    Specific Cast or Director (optional)

    Output:
    Generate a downloadable JSON file with movie details in the following format for each movie:
    {
      "movies": [
        {
          "title": "Title",
          "genre": "Genre",
          "language": "Language",
          "cast": "Cast",
          "director": "Director",
          "cast_names": "Cast names",
          "poster": "Poster URL",
          "tmdb_id": "TMDb ID",
          "release_year":"Original release year"
        },
        {
          "title": "Title",
          "genre": "Genre",
          "language": "Language",
          "cast": "Cast",
          "director": "Director",
          "cast_names": "Cast names",
          "poster": "Poster URL",
          "tmdb_id": "TMDb ID",
          "release_year":"Original release year"
        },
        {
          "title": "Title",
          "genre": "Genre",
          "language": "Language",
          "cast": "Cast",
          "director": "Director",
          "cast_names": "Cast names",
          "poster": "Poster URL",
          "tmdb_id": "TMDb ID",
          "release_year":"Original release year"
        }
      ]
    }

    Important Guideline:
    Do not generate TMDb movie IDs randomly. Go through web and find the accurate tmdb id.
    
    Trigger Prompt:
    When the user provides the input, the tool will execute the recommendation process as specified in the instructions.

    Example Usage:

    Input:
    Genres: Action, Thriller
    Mood: Exciting
    Language: English
    Movie Length: 100-150
    Release Year: 2010-2020
    Specific Cast or Director: Christopher Nolan

    Output:
    {
      "movies": [
        {
          "title": "Inception",
          "genre": "Action, Thriller",
          "language": "English",
          "cast": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page",
          "director": "Christopher Nolan",
          "cast_names": "Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page",
          "poster": "[Poster URL]",
          "tmdb_id": "27205",
          "release_year": "2010"
        },
        {
          "title": "The Dark Knight",
          "genre": "Action, Crime, Drama",
          "language": "English",
          "cast": "Christian Bale, Heath Ledger, Aaron Eckhart",
          "director": "Christopher Nolan",
          "cast_names": "Christian Bale, Heath Ledger, Aaron Eckhart",
          "poster": "[Poster URL]",
          "tmdb_id": "155",
          "release_year": "2008"
        },
        {
          "title": "Interstellar",
          "genre": "Adventure, Drama, Science Fiction",
          "language": "English",
          "cast": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
          "director": "Christopher Nolan",
          "cast_names": "Matthew McConaughey, Anne Hathaway, Jessica Chastain",
          "poster": "[Poster URL]",
          "tmdb_id": "157336", 
          "release_year": "2014"
        }
      ]
    }

    Additional Information:
    Ensure the tool fetches accurate and existing movie details to avoid hallucinations.
    Preferably fetch movies from TMDb but do not limit to it if required data is not available.
    Include capabilities for users to provide feedback for continuous improvement of the tool’s accuracy and functionality.

    Deliverables:
    A working prototype that demonstrates the tool’s ability to recommend three movies based on user inputs.
    Documentation outlining the tool’s capabilities, usage instructions, and information on data handling and accuracy.

    Very important note:
    Any other messages than what's specified must be skipped. For example introduction messages like 'Here are three movie recommendations based on your preferences:' , note messages and conclusion messages must be skipped. Poster link should be valid. Randomize movies for same input. 

    Format:
    Give the result in json format directly without any other beginning messages stating that it is in json. For example, skip "```json"

    Regenerating Movies:
    If the user input consist of "Generate New" in the end, new set of movies must be given but it should follow the given constraints of details.

    User has given the specific input \n 
    """

    model_input=prompt+user_input

    # Use the configured model to generate content
    try:
        responses = model_text.generate_content(model_input)
        movie_data = json.loads(responses.text)
        return movie_data
    except Exception as e:
        return f"Error generating content: {e}"
    