## Step 1 - Import Necessary Libraries ##
import pickle
import streamlit as st
import requests

## Step 2 - Load the Pickle Data we generated from Jupyter Notebook ##
movies = pickle.load(open('movies.pkl', 'rb'))
movie_list = movies['title'].values
similarity = pickle.load(open('similarity.pkl', 'rb'))

## Step 3 - Set the Title and Header of Web page and a SelectBox for Movie Input ##
st.header('Content-Based Movie Recommendation')
selected_movie = st.selectbox("Select a movie you have watched : ",movie_list)

## Step 4 - Create a function to get the poster of the movie from the TMDB database ##
def fetch_poster(id):
    # They provide poster with the id of the movie, API Key needs to be generated first, {} is replaced with the movie id
    data = (requests.get("https://api.themoviedb.org/3/movie/{}?api_key=ceabcb8174e3ee298d76cf914882847d&language=en-US".format(id))).json()
    #The poster path is taken from the generated Json File, and then image is given as the output
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

## Step 5 - Create a function to Recommend the movie based on Similarity (Same as done previously) ##
def recommend(movie):
    index = movies[movies['title'] == movie].index[0] #Get the index of the movie
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1]) #Compute the similarity
    recommended_movie_names = [] #List of Movies
    recommended_movie_posters = [] #List of Poster Path corresponding to the list of movies
    for i in distances[1:13]: #We recommend top 12 movies
        recommended_movie_posters.append(fetch_poster(movies.iloc[i[0]].id)) #Get the poster path from function
        recommended_movie_names.append(movies.iloc[i[0]].title) #Get and store the movie title
    return recommended_movie_names, recommended_movie_posters

## Step 6 - Display the Movie Title and its respective poster ##
if st.button('Show Recommendation'): #If the button is pressed, call the recommend function for the given input
    recommended_movie_names, recommended_movie_posters = recommend(selected_movie)

    #Each row is set with 3 columns, first poster then the text is given as the output
    col1, col2, col3 = st.columns(3)
    with col1:
        st.image(recommended_movie_posters[0])
        st.text(recommended_movie_names[0])
    with col2:
        st.image(recommended_movie_posters[1])
        st.text(recommended_movie_names[1])
    with col3:
        st.image(recommended_movie_posters[2])
        st.text(recommended_movie_names[2])

    col4, col5, col6 = st.columns(3)
    with col4:
        st.image(recommended_movie_posters[3])
        st.text(recommended_movie_names[3])
    with col5:
        st.image(recommended_movie_posters[4])
        st.text(recommended_movie_names[4])
    with col6:
        st.image(recommended_movie_posters[5])
        st.text(recommended_movie_names[5])

    col7, col8, col9 = st.columns(3)
    with col7:
        st.image(recommended_movie_posters[6])
        st.text(recommended_movie_names[6])
    with col8:
        st.image(recommended_movie_posters[7])
        st.text(recommended_movie_names[7])
    with col9:
        st.image(recommended_movie_posters[8])
        st.text(recommended_movie_names[8])

    col10, col11, col12 = st.columns(3)
    with col10:
        st.image(recommended_movie_posters[9])
        st.text(recommended_movie_names[9])
    with col11:
        st.image(recommended_movie_posters[10])
        st.text(recommended_movie_names[10])
    with col12:
        st.image(recommended_movie_posters[11])
        st.text(recommended_movie_names[11])
