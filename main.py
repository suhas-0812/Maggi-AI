from tmdbid import fetch_tmdb_movie_id
from recommend import generate_movie_recommendation_prompt
from tmdbposter import fetch_poster
import streamlit as st

st.title("2 Min Movie Recommendation Test")
st.subheader("Find your next movie in 2 minutes")

page = st.sidebar.radio("Navigation",['Home','Feedback'],index=0)

if page == 'Home':

    # List of genres
    genres_list = ["Action", "Thriller", "Comedy", "Drama", "Romance", "Horror", "Science Fiction", "Fantasy", "Adventure", "Mystery", "Crime", "Animation", "Family", "Biography"]

    # List of moods with emojis
    moods = {
        "😊 Happy": "Happy",
        "😢 Sad": "Sad",
        "😱 Scary": "Scary",
        "😍 Love": "Love",
        "🤔 Thoughtful": "Thoughtful",
        "🎉 Exciting": "Exciting"
    }

    # List of languages
    languages = ["English", "Hindi", "Kannada", "Tamil", "Telugu", "Malayalam"]

    # Streamlit app title
    st.subheader("Select Movie Preferences")

    # Genre selection
    selected_genres = st.multiselect("Select Genres:", genres_list)

    # Mood selection
    selected_mood = st.radio("Select Mood:", list(moods.keys()))

    # Language selection
    selected_language = st.selectbox("Select Language:", languages)

    # Movie length slider
    movie_length = st.slider("Select Movie Length (in minutes):", 60, 270, (90, 150), step=30)

    # Release year slider
    release_year = st.slider("Select Release Year:", 2000, 2024, (2010, 2020), step=5)

    # Specific cast or director input
    specific_cast_or_director = st.text_input("Enter Specific Cast or Director (optional):")

    # Generate the input string
    input_string = f"""
    Genres: {', '.join(selected_genres)}
    Mood: {moods[selected_mood]}
    Language: {selected_language}
    Movie Length: {movie_length[0]}-{movie_length[1]}
    Release Year: {release_year[0]}-{release_year[1]}
    """
    if specific_cast_or_director:
        input_string += f'Specific Cast or Director: "{specific_cast_or_director}"'

    if st.button("Recommend"):

        status_text = st.empty()
        progress_bar = st.progress(0)
        status_text = st.empty()
        status_text.text("Finding Movies Using Gemini")
        progress_bar.progress(20)

        for attempt in range(3):
            recommended_movies = generate_movie_recommendation_prompt(input_string)
            progress_bar.progress(20+attempt*10)
            if isinstance(recommended_movies, dict):
                break  # Exit loop if successful
            else:
                st.write(recommended_movies)

        if isinstance(recommended_movies, dict):
            st.json(recommended_movies)
            status_text.text("Linking movies to TMDb...")
            progress_bar.progress(50)

            i=0

            for movie in recommended_movies['movies']:
                i=1
                movie['tmdb_id']=fetch_tmdb_movie_id(movie['title'], movie['release_year'], movie['language'])
                movie['poster']=fetch_poster(movie['tmdb_id'])
                increment=i*15
                progress_bar.progress(50+increment)
            
            status_text.text('Completed')
            progress_bar.progress(100)

            st.markdown("### Movies For You ")
            index=0
            for movie in recommended_movies['movies']:
                index+=1
                if index==2:
                    col2, col1 = st.columns([2,1])
                else:
                    col1, col2 = st.columns([1,2])
                with col1:
                    if movie['poster']!="Poster not found within the time limit":
                        st.image(movie['poster'])
                    else:
                        st.write("Poster Unavailable")
                with col2:
                    st.subheader(movie['title'])
                    st.write("Release Year: "+movie['release_year'])
                    st.write("Genre: "+movie['genre'])
                    st.write("Language: "+movie['language'])
                    st.write("Cast: "+movie['cast'])
                    st.write("Director: "+movie['director'])
                    st.write("TMDb ID: "+str(movie['tmdb_id']))
            
        else:
            st.write("Error occured due to rate limits. Please try again in some time")

