import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '2e2ab0e592da871eb769e0abfa54e518'
tmdb.language = 'ko-KR'

def find_sim_movie(title_name):
    title_moive = movies[movies['title'] == title_name]
    title_index = title_moive.index.values
    movies['sim'] = cosine_sim[title_index, :].reshape(-1, 1)
    # 검색 대상은 제외하기 위해 1부터 10개 출력
    temp = movies.sort_values(['sim', 'weighted'], ascending = False)
    temp = temp[temp.index.values != title_index]
    final_index = temp.index.values[:10]
    images, titles = [], []
    for i in final_index:
        id = movies['id'].iloc[i]
        # movie.details()는 tmdbv3api에서 지원하는 메서드로 id를 입력하면 해당 영화 정보를 표시
        # 자세한 사항은 구글에 tmdb movie details 검색
        detail = movie.details(id)
        image_path = detail['poster_path']
        if image_path:
            image_path = 'https://image.tmdb.org/t/p/w500' + image_path
        else:
            image_path = 'no_image.jpg'
        images.append(image_path)
        titles.append(detail['title'])
    return images, titles

movies = pickle.load(open('movie_df.pickle', 'rb'))
cosine_sim = pickle.load(open('cosine_sim.pickle', 'rb'))

st.set_page_config(layout='wide')
st.header('영화추천시스템')

movie_list = movies['title'].values
title = st.selectbox('좋아하는 영화를 입력하세요.', movie_list)

if st.button('추천'):
    with st.spinner('로딩중...'):
        images, titles = find_sim_movie(title)
        
        idx = 0 # 열번호
        for i in range(0, 2): # 행번호
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1

import subprocess
import sys

def run_streamlit():
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    run_streamlit()