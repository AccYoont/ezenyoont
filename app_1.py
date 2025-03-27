import os
import sys
import pickle
import streamlit as st
from tmdbv3api import Movie, TMDb

# PyInstaller 실행 환경을 고려한 경로 설정
def get_path(filename):
    if hasattr(sys, '_MEIPASS'):  # PyInstaller 실행 환경인지 확인
        return os.path.join(sys._MEIPASS, filename)
    return filename  # 개발 환경에서는 그대로 사용

movie = Movie()
tmdb = TMDb()
tmdb.api_key = '2e2ab0e592da871eb769e0abfa54e518'
tmdb.language = 'ko-KR'

def find_genres_movie(title_name):
    title_moive = movies[movies['title'] == title_name]
    title_genres = title_moive['genres'].tolist()[0]
    temp = movies[movies['genres'].apply(lambda x : any(genres in x for genres in title_genres))]
    temp = temp.sort_values('popularity', ascending=False).iloc[:10]
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


# 데이터 로드
movies = pickle.load(open(get_path('movie_df1.pickle'), 'rb'))

st.set_page_config(layout='wide')
st.header('영화추천시스템')

movie_list = movies['title'].values
title = st.selectbox('좋아하는 영화를 입력하세요.', movie_list)

# if문의 수정
if st.button('추천'):
    with st.spinner('로딩중...'):
        images, titles = find_genres_movie(title)
        
        idx = 0 # 열번호
        for i in range(0, 2): # 행번호
            cols = st.columns(5)
            for col in cols:
                col.image(images[idx])
                col.write(titles[idx])
                idx += 1