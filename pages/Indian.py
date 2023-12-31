######################################################## Import Packages ########################################################

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import streamlit as st
import sys, path
import requests
from pathlib import Path
import os


api_key = st.secrets['api_key']

######################################################### Import Dataset #########################################################

dir = path.Path(__file__)
sys.path.append(dir.parent.parent)
path_1 = Path(__file__).parent / '../Dataset/Indian_with_Poster.csv'
path_2 = Path(__file__).parent / '../Dataset/Indian_Similarity.pkl'
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
    return INDIAN_MOVIE[['imdb_title_id', 'original_title', 'Poster']].iloc[movie_indices]

@st.cache_data
def MOVIES_LIST_INDIA():
    return tuple(INDIAN_MOVIE['original_title'])



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

IMDB_LINK = "https://www.imdb.com/title/"

POSTER = []
MOVIE_LINK = []
if st.button('RECOMMEND'):
    RECOMMENDED_MOVIE = get_recommendations_india(USER_INPUT)[['Poster', 'imdb_title_id']]
    for Poster in RECOMMENDED_MOVIE['Poster']:
        POSTER.append(Poster) 
    for id in RECOMMENDED_MOVIE['imdb_title_id']:
        MOVIE_LINK.append(f"{IMDB_LINK}{id}")

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
    
    movie_name = USER_INPUT
    image_url = INDIAN_MOVIE[INDIAN_MOVIE['original_title'] == movie_name]['Poster'].values[0]
    imdb_id = INDIAN_MOVIE[INDIAN_MOVIE['original_title'] == movie_name]['imdb_title_id'].values[0]
    poster_url = f"{IMDB_LINK}{imdb_id}"
    custom_css = """
    <style>
            .centered-image-container {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 0px;
            }

            .centered-image {
                display: block;
                margin-left: auto;
                padding: 10px;
                box-sizing: border-box;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5);
                margin-right: auto;
                margin-bottom: 40px;
                transition: box-shadow 0.3s ease-in-out;
            }

            .centered-image:hover {
                box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.7);
                background-color: #13315c;
            }
        </style>
    """ 
    image_width = 350
    image_height = 500
    html_code = f"""
    <div class="centered-image-container">
        <a href="{poster_url}">
            <img class="centered-image" src="{image_url}" alt="Centered Image" width="{image_width}" height="{image_height}">
        </a>
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

    Recommended_Poster = """
        <style>
            .image-row {
                display: flex;
                flex-wrap: wrap;
                justify-content: center;
            }

            .image-item {
                width: 30%;
                padding: 10px;
                box-sizing: border-box;
                box-shadow: 0 4px 8px 0 rgba(0, 0, 0, 0.5);
                height: auto;
                max-width: 328px;
                margin: 10px;
                text-align: center;
                transition: box-shadow 0.3s, background-color 0.3s;
            }

            .image-item:hover {
                box-shadow: 0 8px 16px 0 rgba(0, 0, 0, 0.8);
                background-color: #13315c;
            }

            .image-item img {
                width: 100%;
                height: auto;
                object-fit: cover;
                border: 1px solid #ccc;
                cursor: pointer;
            }
        </style>
    """
    Recommended_Body = f"""
        <div class="image-row">
            <div class="image-item">
                <a href = "{MOVIE_LINK[0]}">
                    <img src="{POSTER[0]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[1]}">
                    <img src="{POSTER[1]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[2]}">
                    <img src="{POSTER[2]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[3]}">
                    <img src="{POSTER[3]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[4]}">
                    <img src="{POSTER[4]}" "alt="Image 1">
                </a>    
            </div>
        </div>
        <div class="image-row">
            <div class="image-item">
                <a href = "{MOVIE_LINK[5]}">
                    <img src="{POSTER[5]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[6]}">
                    <img src="{POSTER[6]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[7]}">
                    <img src="{POSTER[7]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[8]}">
                    <img src="{POSTER[8]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[9]}">
                    <img src="{POSTER[9]}" "alt="Image 1">
                </a>    
            </div>
        </div>
        <div class="image-row">
            <div class="image-item">
                <a href = "{MOVIE_LINK[10]}">
                    <img src="{POSTER[10]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[11]}">
                    <img src="{POSTER[11]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[12]}">
                    <img src="{POSTER[12]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[13]}">
                    <img src="{POSTER[13]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[14]}">
                    <img src="{POSTER[14]}" "alt="Image 1">
                </a>    
            </div>
        </div>
        <div class="image-row">
            <div class="image-item">
                <a href = "{MOVIE_LINK[15]}">
                    <img src="{POSTER[15]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[16]}">
                    <img src="{POSTER[16]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[17]}">
                    <img src="{POSTER[17]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[18]}">
                    <img src="{POSTER[18]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[19]}">
                    <img src="{POSTER[19]}" "alt="Image 1">
                </a>    
            </div>
        </div>
        <div class="image-row">
            <div class="image-item">
                <a href = "{MOVIE_LINK[20]}">
                    <img src="{POSTER[20]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[21]}">
                    <img src="{POSTER[21]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[22]}">
                    <img src="{POSTER[22]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[23]}">
                    <img src="{POSTER[23]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[24]}">
                    <img src="{POSTER[24]}" "alt="Image 1">
                </a>    
            </div>
        </div>
        <div class="image-row">
            <div class="image-item">
                <a href = "{MOVIE_LINK[25]}">
                    <img src="{POSTER[25]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[26]}">
                    <img src="{POSTER[26]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[27]}">
                    <img src="{POSTER[27]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[28]}">
                    <img src="{POSTER[28]}" "alt="Image 1">
                </a>    
            </div>
            <div class="image-item">
                <a href = "{MOVIE_LINK[29]}">
                    <img src="{POSTER[29]}" "alt="Image 1">
                </a>    
            </div>
        </div>
    """

    st.markdown(Recommended_Poster, unsafe_allow_html=True)
    st.markdown(Recommended_Body, unsafe_allow_html=True)

    POSTER.clear()
    st.cache_data.clear()