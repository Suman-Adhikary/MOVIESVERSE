######################################################## Import Packages ########################################################

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import streamlit as st
import sys, path
import requests
from pathlib import Path
import os



######################################################### Import Dataset #########################################################

dir = path.Path(__file__)
sys.path.append(dir.parent.parent)
path_1 = Path(__file__).parent / '../Dataset/IMDB_Indian.csv'
path_2 = Path(__file__).parent / '../Dataset/Indian IMDB Similarity.pkl'
INDIAN_MOVIE = pd.read_csv(path_1, lineterminator='\n')
INDIAN_SIMILARITY = pd.read_pickle(path_2)



tfidf_india = TfidfVectorizer(stop_words='english')
INDIAN_MOVIE['Combined'] = INDIAN_MOVIE['Combined'].fillna('')
tfidf_matrix_ind = tfidf_india.fit_transform(INDIAN_MOVIE['Combined'])
cosine_sim_india = linear_kernel(tfidf_matrix_ind, tfidf_matrix_ind)


@st.cache_data
def get_recommendations_india(title, cosine_sim=cosine_sim_india):
    idx = INDIAN_SIMILARITY[title]
    sim_scores = list(enumerate(cosine_sim_india[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:35]
    movie_indices = [i[0] for i in sim_scores]
    return INDIAN_MOVIE[['imdb_title_id', 'original_title', 'Combined']].iloc[movie_indices]

@st.cache_data
def MOVIES_LIST_INDIA():
    return tuple(INDIAN_MOVIE['title'])



########################################################## STREAMLIT WEBPAGE #####################################################

st.set_page_config(layout="wide", page_title="Movie Recommeded System")
st.write('<style>div.block-container{padding-top:0rem;}</style>', unsafe_allow_html=True)

@st.cache_data
def Main_Header():
    header_css = """
    <head>
    <link rel="stylesheet" href="https://fonts.googleapis.com/css?family=Noto Sans Display">
        <style>
            h1 {
                font-family: 'Noto Sans Display';
                text-align: center;
                font-size: 60px;
                margin-bottom: 0px;
            }
            .word1 {
                color: #696eff;
            }

            .word2 {
                color: #f8acff;
            }

            .word3 {
                color: #696eff;
            }
        </style>
    </head>
    """

    Main_head = """
        <h1>
            <span class="word1">MOVIE</span>
            <span class="word2">RECOMMENDED</span>
            <span class="word3">SYSTEM</span>
        </h1>
    """
    st.markdown(header_css, unsafe_allow_html=True)
    st.markdown(Main_head, unsafe_allow_html=True)
    st.markdown(
        """
        <div style="text-align:center;">
            <a style="margin-right: 16px;"><img src="https://img.icons8.com/?size=256&id=ortlsYTZxMvT&format=png" alt="Netflix" width="40" height="40"></a>
            <a style="margin-right: 16px;"><img src="https://img.icons8.com/?size=256&id=mJTj7Q9EPSVn&format=png" alt="Amazon Prime Video" width="40" height="40"></a>
            <a style="margin-right: 16px;"><img src="https://img.icons8.com/?size=256&id=19318&format=png" alt="YouTube" width="40" height="40"></a>
            <a style="margin-right: 16px;"><img src="https://img.icons8.com/?size=256&id=GJTUa9i8YZ5Y&format=png" alt="Disney" width="40" height="40"></a>
            <a style="margin-right: 16px;"><img src="https://img.icons8.com/?size=256&id=7Vg5ZDdi9vV5&format=png" alt="Apple TV" width="40" height="40"></a>
            <a><img src="https://img.icons8.com/?size=256&id=ITiDg1AcK044&format=png" alt="IMDb" width="30" height="30"></a>
        </div>
        """,
        unsafe_allow_html=True)
    
Main_Header()

@st.cache_data
def process_input(input_value):
    result = input_value
    return result


GET_IMDB_ID = INDIAN_MOVIE.set_index('original_title')['imdb_title_id'].to_dict()
MOVIES_SELECTION = st.selectbox('ENTER A MOVIE NAME', MOVIES_LIST_INDIA(), placeholder="🎞️SEARCH OR SELECT A MOVIE🎞️", label_visibility='hidden')
USER_INPUT = process_input(MOVIES_SELECTION)

POSTER = []
TMDB_ID = []
if st.button('RECOMMEND'):
    RECOMMENDED_MOVIE = get_recommendations_india(USER_INPUT)['imdb_title_id']
    for ID in RECOMMENDED_MOVIE:
        TMDB_ID.append(ID)
    for i in TMDB_ID:
        movie_id = i
        base_url = 'https://api.themoviedb.org/3'
        response = requests.get(f'{base_url}/movie/{movie_id}?api_key={api_key}')

        if response.status_code == 200:
            movie_data = response.json()
            poster_path = movie_data['poster_path']
            poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
            POSTER.append(poster_url)                     

    css_viz = """
    <style>
        h4{
            padding: 0px 0;
            font-size: 45px;
            color: blue;
            text-align: center;
        }
        .rainbow-divider {
            height: 1px;
            background: #1B2457;
            margin: -20px 0;
            margin-top : 5px;
            margin-bottom: 30px;
        } 
    </style>
    """

    vi_head = """
        <h4>
        WATCHED MOVIE 
        </h4>
    """
    st.markdown(css_viz, unsafe_allow_html=True)
    st.markdown(vi_head, unsafe_allow_html=True)        
    
    movie_name = GET_IMDB_ID[USER_INPUT]
    movie_id = movie_name
    base_url = 'https://api.themoviedb.org/3'
    response = requests.get(f'{base_url}/movie/{movie_id}?api_key={api_key}')

    if response.status_code == 200:
        movie_data = response.json()
        poster_path = movie_data['poster_path']
        poster_url = f'https://image.tmdb.org/t/p/original{poster_path}'
        custom_css = """
        <style>
            .centered-image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 0px 0;
            }
            .centered-image {
                display: block;
                margin-left: auto;
                margin-right: auto;
                margin-bottom: 40px;
            }
        </style>
        """ 
        image_width = 250
        image_height = 400
        html_code = f"""
        <div class="centered-image-container">
            <img class="centered-image" src="{poster_url}" alt="Centered Image" width="{image_width}" height="{image_height}">
        </div>
        """
        st.markdown(custom_css, unsafe_allow_html=True)
        st.markdown(html_code, unsafe_allow_html=True)             

    VI_head = """
        <h4>
            RECOMMENDED MOVIE
        </h4>
        <div class = "rainbow-divider"></div>
    """  
    st.markdown(css_viz, unsafe_allow_html=True)
    st.markdown(VI_head, unsafe_allow_html=True)         

    col1, col2, col3, col4, col5, col6, col7, col8, col9, col10 = st.columns(10)
    with col1:
        st.image(POSTER[0])
    with col2:
        st.image(POSTER[1])
    with col3:
        st.image(POSTER[2])
    with col4:
        st.image(POSTER[3])
    with col5:
        st.image(POSTER[4])
    with col6:
        st.image(POSTER[5])
    with col7:
        st.image(POSTER[6])
    with col8:
        st.image(POSTER[7])
    with col9:
        st.image(POSTER[8])
    with col10:
        st.image(POSTER[9])

    col11, col12, col13, col14, col15, col16, col17, col18, col19, col20 = st.columns(10)
    with col11:
        st.image(POSTER[10])
    with col12:
        st.image(POSTER[11])
    with col13:
        st.image(POSTER[12])
    with col14:
        st.image(POSTER[13])
    with col15:
        st.image(POSTER[14])
    with col16:
        st.image(POSTER[15])
    with col17:
        st.image(POSTER[16])
    with col18:
        st.image(POSTER[17])
    with col19:
        st.image(POSTER[18])
    with col20:
        st.image(POSTER[19])

    col21, col22, col23, col24, col25, col26, col27, col28, col29, col30 = st.columns(10)
    with col21:
        st.image(POSTER[20])
    with col22:
        st.image(POSTER[21])
    with col23:
        st.image(POSTER[22])
    with col24:
        st.image(POSTER[23])
    with col25:
        st.image(POSTER[24])
    with col26:
        st.image(POSTER[25])
    with col27:
        st.image(POSTER[26])
    with col28:
        st.image(POSTER[27])
    with col29:
        st.image(POSTER[28])
    with col30:
        st.image(POSTER[29])

    TMDB_ID.clear()    
    POSTER.clear()   
    st.cache_data.clear() 