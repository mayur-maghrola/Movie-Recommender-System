'''
Team : InovateX 💢
Offline version without API calls
'''

import pickle
import streamlit as st

def get_placeholder_poster():
    """Return a placeholder image URL when API is unavailable"""
    return "https://via.placeholder.com/500x750/0066cc/ffffff?text=Movie+Poster"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    
    for i in distances[1:6]:
        movie_title = movies.iloc[i[0]].title
        recommended_movie_names.append(movie_title)
        # Use placeholder instead of API call
        recommended_movie_posters.append(get_placeholder_poster())

    return recommended_movie_names, recommended_movie_posters

st.header('🎬 Movie Recommender System Using Machine Learning')

try:
    movies = pickle.load(open('artifacts/movie_list.pkl','rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl','rb'))
except FileNotFoundError:
    st.error("Model files not found. Please run the Jupyter notebook first to generate the required files.")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox(
    "Type or select a movie from the dropdown 👇",
    movie_list
)

if st.button('Show Recommendation'):
    with st.spinner('Getting recommendations...'):
        recommended_movie_names, recommended_movie_posters = recommend(selected_movie)
        
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(recommended_movie_names[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_names[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended_movie_names[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_names[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_names[4])
        st.image(recommended_movie_posters[4])

st.info("💡 This is the offline version. For movie posters, use the main portal.py after fixing network issues.")