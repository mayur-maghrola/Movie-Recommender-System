'''
Team : InovateX 💢
'''

import pickle
import os
import gdown
import streamlit as st
import requests

def download_models():
    os.makedirs('artifacts', exist_ok=True)
    if not os.path.exists('artifacts/movie_list.pkl'):
        gdown.download('https://drive.google.com/uc?id=1i2NiwmRNLmJr01--Q1D2S6YM3T_cY7jZ', 'artifacts/movie_list.pkl', quiet=False)
    if not os.path.exists('artifacts/similarity.pkl'):
        gdown.download('https://drive.google.com/uc?id=1ETtxHSkY7P9e09SV328MrTUNIholMdZF', 'artifacts/similarity.pkl', quiet=False)

def fetch_poster(movie_id):
    try:
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        response = requests.get(url, timeout=5)
        if response.status_code == 200:
            data = response.json()
            poster_path = data.get('poster_path')
            if poster_path:
                return "https://image.tmdb.org/t/p/w500/" + poster_path
        return "https://via.placeholder.com/500x750/cccccc/000000?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750/cccccc/000000?text=No+Image"

def recommend(movie):
    index = movies[movies['title'] == movie].index[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_movie_names = []
    recommended_movie_posters = []
    for i in distances[1:6]:
        movie_id = movies.iloc[i[0]].movie_id
        recommended_movie_posters.append(fetch_poster(movie_id))
        recommended_movie_names.append(movies.iloc[i[0]].title)
    return recommended_movie_names, recommended_movie_posters

st.write("InnovateX 💢")
st.header('🎬 Movie Recommender System Using Machine Learning')

with st.spinner('Loading model files...'):
    download_models()

try:
    movies = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
    similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
except Exception as e:
    st.error(f"Failed to load model files: {e}")
    st.stop()

movie_list = movies['title'].values
selected_movie = st.selectbox("Type or select a movie from the dropdown 👇", movie_list)

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
