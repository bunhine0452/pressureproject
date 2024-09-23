import pandas as pd
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from imblearn.over_sampling import SMOTENC
import joblib
import pickle
import os
from fpdf import FPDF
from io import BytesIO
import json

# funcs.py
from funcs import load_css, load_local_font, linegaro, linesero, csv , calculate_proportions , remove_outliers ,calculate_alcohol_score, calculate_physical_activity_score, calculate_whtR_category

# 페이지 로드
from info import info_page 
from dashboard import dashboard_page
from model_test import model_test_page
from form import form_page
# 페이지 설정
st.set_page_config(page_title='❤️‍🩹고혈의 고혈압', page_icon='❤️‍🩹', layout='wide')


# 외부 CSS 불러오기
load_css('./style.css')
# 폰트 설정
load_local_font('AppleSDGothicNeoB', './fonts/AppleSDGothicNeoB.ttf')


# 사이드바 타이틀
st.sidebar.title('🏷️')
# 페이지 선택 함수 맵핑
page_select = {
    "팀 소개 및 목표": info_page,  # 괄호 없이 함수 참조 전달
    "데이터 살펴보기": dashboard_page,
    "모델 테스트 결과": model_test_page,
    "나의 고혈압 확률 예측해보기": form_page,
}

# 사이드바에서 페이지 선택
st.sidebar.markdown("<p style='color: #efebe7; font-size: 25px;'>Select a page</p>", unsafe_allow_html=True)
selected_page = st.sidebar.radio("이동하기", page_select.keys(), key="value")
page_select[selected_page]()
st.sidebar.markdown(
    """
    <a href="https://highbloodpressure.streamlit.app" target="_blank">
        👉 웹사이트로 이동하기
    </a>
    """, 
    unsafe_allow_html=True
)