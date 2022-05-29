import pickle
import streamlit as st
import requests
import pandas as pd
import requests
from PIL import Image
from streamlit_option_menu import option_menu
import json
from streamlit_lottie import st_lottie




#---------- setting the width-------------#
st.set_page_config(layout="wide")



#------------fetching the posters-----------#

def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    response = requests.get(url)
    data = response.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

#----------functions for recommendations--------#


        #------perfection------#


def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters

        #--------genres---------#

def recommend1(movie):
    movie_index = movies1[movies1['title'] == movie].index[0]
    distances = similarity1[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters

        #-------cast----------#
def recommend2(movie):
    movie_index = movies2[movies1['title'] == movie].index[0]
    distances = similarity2[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:7]
    recommended_movies = []
    recommended_movie_posters = []
    for i in movies_list:
        # fetch the movie poster
        movie_id = movies.iloc[i[0]].movie_id

        recommended_movies.append(movies.iloc[i[0]].title)

        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended_movies,recommended_movie_posters




st.markdown("<h1 style='text-align: left; color: #EA3839;'>Everyday Movies</h1>", unsafe_allow_html=True)

st.markdown("<h8 style='text-align: left; color: white;'> Are you too tired to search a perfect movie for yourself daily ? <br> don't worry  this web app does exactly this for you.</h8>", unsafe_allow_html=True)

#--------------navbar-----------#
with st.sidebar:
    selected = option_menu("Main Menu", ["Home","Recommendation based on:","Perfection",' Genres','Movie Cast','My favourites','My Account','Write to us','Settings'],
                           icons=['house','heart',' ',',',' ','star','square','pencil','gear'], menu_icon="cast", default_index=1)



    #---------------- animation------------------#

def load_lottiefile(url:str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


lottie_hello = load_lottiefile("https://assets3.lottiefiles.com/private_files/lf30_bb9bkg1h.json")
st_lottie(lottie_hello, key =" watching")





movies_dict= pickle.load(open('movie_dict.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

movies_dict1 = pickle.load(open('movie_dict_cast.pkl','rb'))
movies1 = pd.DataFrame(movies_dict1)
similarity1 = pickle.load(open('similarity_cast.pkl','rb'))

movies_dict2 = pickle.load(open('movie_dict_genres.pkl','rb'))
movies2 = pd.DataFrame(movies_dict2)
similarity2 = pickle.load(open('similarity_genres.pkl','rb'))


#-----------select box-----------#

selected_movie_name  = st.selectbox(
    "Enter or type the name of the movie similiar to which you wish to watch today to get the perfect recommendations.",
    set(movies['title'].values)
)








#-------Use local CSS--------#

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style.css")





 #-----------Display----------#
def create_grid_view_for_movies(recommended_movie_name,recommended_movie_posters):
    col1, col2, col3 = st.columns(3)
    col4, col5, col6 = st.columns(3)
    with col1:
        st.text(recommended_movie_name[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended_movie_name[1])
        st.image(recommended_movie_posters[1])

    with col3:
        st.text(recommended_movie_name[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended_movie_name[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended_movie_name[4])
        st.image(recommended_movie_posters[4])
    with col6:
        st.text(recommended_movie_name[5])
        st.image(recommended_movie_posters[5])

#--------------recommender button  and main function callings------------#

if st.button('Show Recommendations'):
    with st.container():
        left_column,right_column = st.columns(2)
        with left_column:
             st.markdown("<h3 style='text-align: center; color: grey;'><br><br>Grab your snacks and dive into the movies<br><br></h3>", unsafe_allow_html=True)
        with right_column:
            lottie_snack = load_lottiefile("https://assets5.lottiefiles.com/packages/lf20_cbrbre30.json")
            st_lottie(lottie_snack, key=" snacks",height=300)


    st.markdown(
        "<h3 style='text-align: center; color: grey;'><br><br>Perfect recommendations for you<br><br></h3>",
        unsafe_allow_html=True)

    recommended_movie_name,recommended_movie_posters = recommend(selected_movie_name)
    create_grid_view_for_movies(recommended_movie_name,recommended_movie_posters)

    st.markdown(
        "<h3 style='text-align: center; color: grey;'><br><br>Recommended on basis of genres similar to movie you selected<br><br></h3>",unsafe_allow_html=True)

    recommended_movie_name, recommended_movie_posters = recommend2(selected_movie_name)
    create_grid_view_for_movies(recommended_movie_name, recommended_movie_posters)

    st.markdown(
        "<h3 style='text-align: center; color: grey;'><br><br>Recommended on basis of cast similar to movie you selected<br><br></h3>",unsafe_allow_html=True)

    recommended_movie_name, recommended_movie_posters = recommend1(selected_movie_name)
    create_grid_view_for_movies(recommended_movie_name, recommended_movie_posters)

#------------write to us--------------#

    with st.container():
        st.markdown(
            "<h3 style='text-align: center; color: grey;'><br><br>We will be happy to hear from u <br><br></h3>",unsafe_allow_html=True)

        st.write("Write us your Queries or reviews")
        contact_form = """
            <form action="https://formsubmit.co/chakshumahajan5@gmail.com" method="POST">
                <input type="hidden" name="_captcha" value="false">
                <input type="text" name="name" placeholder="Your name" required>
                <input type="email" name="email" placeholder="Your email" required>
                <textarea name="message" placeholder="Your message here" required></textarea>
                <button type="submit">Send</button>
            </form>
            """

        left_column,right_column = st.columns(2)
        with left_column:
            st.markdown(contact_form, unsafe_allow_html=True)
        with right_column:
            #lottie_write = load_lottiefile("https://assets2.lottiefiles.com/packages/lf20_ljx86sv6.json")
            lottie_write = load_lottiefile("https://assets6.lottiefiles.com/packages/lf20_akvycwlq.json")

            st_lottie(lottie_write, key="write", height=300,speed=2)