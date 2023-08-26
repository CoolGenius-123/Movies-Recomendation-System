# using streamlit to create a web app for movie recommendation system

import streamlit as st
import pandas as pd
import pickle
import requests

# creating a function to fetch the poster path of the movie using the movie_id

def fetch_poster(movie_id):
    
    data = requests.get("https://api.themoviedb.org/3/movie/{}?api_key=6aa58baed4ff4058098e0d3f90d4112b&language=en-US".format(movie_id))
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

# creating a function to recommend movies
def recommend(movie):
        # getting the index of the movie
        movie_index = movies_list[movies_list['title'] == movie].index[0]
        
        # getting the similarity scores of all movies with that movie
        # enumerate() is used to combine the index of the movie along with the similarity score
        similar_movies = list(enumerate(similarity[movie_index]))
        
        # sorting the list of similar movies in descending order
        sorted_similar_movies = sorted(similar_movies, key = lambda x:x[1], reverse = True)
        
        # getting the top 5 similar movies
        top_5_similar_movies = sorted_similar_movies[1:6]
        
        # creating recommended list
        recommended = []
        movie_id = []
        # printing the top 5 similar movies
        for i in range(len(top_5_similar_movies)):
            # fetching movie_id
            movie_id.append(movies_list['movie_id'][top_5_similar_movies[i][0]])
            recommended.append(movies_list['title'][top_5_similar_movies[i][0]])
            
        return recommended, movie_id


# loading the similarity matrix

similarity = pickle.load(open('similarity.pkl', 'rb'))

# loading movies list from movies.pkl file

movies_list = pickle.load(open('movies.pkl', 'rb'))

# accessing the title of movies

titles = movies_list['title'].values

# creating a title for the web app
st.title('Movie Recommendation System')

# creating a selectbox to select a movie
option = st.selectbox('Select a movie', titles)

# adding button to select the movie

if st.button('Recommend'):
    st.write('Top 5 Similar Movies')
    
    rcd, ids = recommend(option)
    # fetching the poster path of the movie_id in ids
    # and displaying the poster along with the movie title collected wise
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        st.text(rcd[0].title()) # converting the first letter of the movie to capital
        st.image(fetch_poster(int(ids[0]))) # converting the string to integer and passing it to the function to fetch the poster path
    
    with col2:
        st.text(rcd[1].title())
        st.image(fetch_poster(int(ids[1])))
    
    with col3:
        st.text(rcd[2].title())
        st.image(fetch_poster(int(ids[2])))
    
    with col4:
        st.text(rcd[3].title())
        st.image(fetch_poster(int(ids[3])))
        
    with col5:
        st.text(rcd[4].title())
        st.image(fetch_poster(int(ids[4])))