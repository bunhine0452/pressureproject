import os 
import pandas as pd
import streamlit as st
import base64
import numpy as np
# css
def load_css(file_name):
    with open(file_name ,encoding='utf-8') as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
# 폰트
def font_to_base64(font_path):
    with open(font_path, "rb") as font_file:
        encoded = base64.b64encode(font_file.read()).decode('utf-8')
    return encoded

# base64로 인코딩된 폰트를 HTML로 삽입
def load_local_font(font_name, font_path):
    font_data = font_to_base64(font_path)
    font_css = f"""
    <style>
    @font-face {{
        font-family: '{font_name}';
        src: url(data:font/ttf;base64,{font_data}) format('truetype');
    }}
    html, body, [class*="css"]  {{
        font-family: '{font_name}', sans-serif;
    }}
    </style>
    """
    st.markdown(font_css, unsafe_allow_html=True)
# 줄 가로,세로
def linegaro():
    st.markdown(
        """
        <div style="border-top: 3px solid #D4BDAC; width: 100%;"></div>
        """,
        unsafe_allow_html=True)
def linesero():
    st.markdown(
        """
        <div style="border-right: 3px solid #D4BDAC; height: flex;"></div>
        """,
        unsafe_allow_html=True
    )

# csv
def csv(what):
    if what=='train':
        return pd.read_csv('./data/csv/train.csv', encoding='utf-8')

    elif what=='test':
        return pd.read_csv('./data/csv/test.csv', encoding='utf-8')
    
    elif what=='all':
        return pd.read_csv('./data/csv/pridicted_df.csv', encoding='utf-8')
    

# 대시보드 그래프 그릴때 이상치 제거
def remove_outliers(df, column, threshold=1.5):
    Q1 = df[column].quantile(0.25)
    Q3 = df[column].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - threshold * IQR
    upper_bound = Q3 + threshold * IQR
    return df[(df[column] >= lower_bound) & (df[column] <= upper_bound)]
# 비율 계산
def calculate_proportions(df, column, bins=None, categories=None):
    if bins is not None:
        df[column] = pd.cut(df[column], bins=bins)
        
    counts = df.groupby([column, 'Target']).size().unstack(fill_value=0)
    proportions = counts[1] / (counts[0] + counts[1])
    proportions = proportions.dropna()
    proportions = proportions.sort_index()

    if categories:
        proportions = proportions.reindex(categories)

    return proportions


# 음주점수 계산 함수
def calculate_alcohol_score(ever_al,how_al,ones_al,wasted_al,stop_al,therapy_al):
            평생음주경험_점수 = {'마시지 않는다': 0, '마신다': 1}.get(ever_al, np.nan)
            음주빈도_점수 = {
                "최근 1년간 전혀 마시지 않았다.": 0,
                "월1회미만": 2,
                "월1회정도": 4,
                "월2~4회": 8,
                "주2~3회 정도": 16,
                "주 4회 이상": 32
            }.get(how_al,0)
            
            한번음주량_점수 = {
                "1-2잔": 2,
                "3-4잔": 4,
                "5-6잔": 8,
                "7-9잔": 16,
                "10잔 이상": 32
            }.get(ones_al,0)
            
            폭음빈도_점수 = {
                "전혀 없음": 0,
                "월 1회 미만": 4,
                "월 1회 정도": 8,
                "주 1회 정도": 16,
                "거의 매일": 32
            }.get(wasted_al,0)
            
            권고여부_점수 = {
                "없음": 0,
                "가족/의사 권고": 8,
                "가족/의사 강력 권고": 16
            }.get(stop_al, 0)
            
            상담여부_점수 = {"있음": 16, "없음": 0}.get(therapy_al,0)


            음주_점수 =  (
                평생음주경험_점수 + 음주빈도_점수 + 한번음주량_점수 + 폭음빈도_점수 +
                권고여부_점수 + 상담여부_점수
            )
            
            if 평생음주경험_점수 == 0:
                음주_점수 = 0

            return 음주_점수

# 신체활동 점수 계산 함수
def calculate_physical_activity_score(high_do,high_days,high_hour,high_min,mid_do,mid_days,mid_hour,mid_min,walk_do,walk_days,walk_hour,walk_min):
            """신체활동 점수를 계산하는 함수"""
            장소이동_점수 = (
                walk_days *
                (walk_hour * 60 + walk_min)
            )
            if walk_do == "안 한다":
                장소이동_점수 = 0
            
            고강도신체활동점수 = (
                high_days *
                (high_hour * 60 + high_min)
            )
            if high_do == "안 한다":
                고강도신체활동점수 = 0
            
            중강도신체활동점수 = (
                mid_days *
                (mid_hour * 60 + mid_min)
            )
            if mid_do == "안 한다":
                중강도신체활동점수 = 0
            
            신체활동점수 = (
                중강도신체활동점수 * 2 +
                고강도신체활동점수 * 3 +
                장소이동_점수
            )
            
            if np.isnan(중강도신체활동점수) and np.isnan(고강도신체활동점수) and np.isnan(장소이동_점수):
                신체활동점수 = np.nan

            return 신체활동점수

# WhtR 카테고리 계산 함수
def calculate_whtR_category(gender,waist,height):
            """WHtR 카테고리 계산 함수"""
            WHtR = waist / height
            if gender == "남자":
                if WHtR <= 0.43:
                    return 0
                elif WHtR <= 0.53:
                    return 1
                elif WHtR <= 0.58:
                    return 2
                elif WHtR <= 0.63:
                    return 3
                elif WHtR <= 0.68:
                    return 4
                else:
                    return 5
            else:  # 여자
                if WHtR <= 0.42:
                    return 0
                elif WHtR <= 0.49:
                    return 1
                elif WHtR <= 0.54:
                    return 2
                elif WHtR <= 0.59:
                    return 3
                elif WHtR <= 0.64:
                    return 4
                else:
                    return 5
                
def cal_waist_ideal(height, gender,inch):
    """
    주어진 신장(cm)과 성별에 따라 이상적인 허리둘레 범위를 계산하는 함수입니다.

    Parameters:
        height_cm (float): 신장(cm)
        gender (str): 성별 ("남자" 또는 "여자")

    Returns:
        tuple: (최소 허리둘레(cm), 최대 허리둘레(cm))
    """
    if gender == "남성":
        WHtR_min = 0.43
        WHtR_max = 0.50
    elif gender == "여성":
        WHtR_min = 0.42
        WHtR_max = 0.47
    else:
        raise ValueError("성별은 '남자' 또는 '여자'로 입력해주세요.")

    if inch == True:
        waist_min = height * WHtR_min / 2.54
        waist_max = height * WHtR_max / 2.54
    else:
        waist_min = height * WHtR_min
        waist_max = height * WHtR_max

    return {'waist_min': waist_min, 'waist_max': waist_max}
                
# model 결과 선택 함수
def model_result(model):
        if model == 'Logistic Regression':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/logi/logi1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/logi/logi2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/logi/logi3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/logi/logi4.png')
        
        elif model == 'SVM':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/svm/svm1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/svm/svm2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/svm/svm3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/svm/svm4.png')

        
        elif model == 'LGBM':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/lgbm/lgbm1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/lgbm/lgbm2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/lgbm/lgbm3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/lgbm/lgbm4.png')
        

        elif model == 'Random Forest':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/rb/rb1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/rb/rb2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/rb/rb3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/rb/rb4.png')
        
        elif model == 'xg':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/xg/xg1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/xg/xg2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/xg/xg3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/xg/xg4.png')

# 하이퍼 파라미터 튜닝 실행                 
def model_result_hyper(model):
        if model == 'Logistic Regression':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/logi/hyper/logihyper1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/logi/hyper/logihyper2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/logi/hyper/logihyper3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/logi/hyper/logihyper4.png')
        
        elif model == 'SVM':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/svm/hyper/svmhyper1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/svm/hyper/svmhyper2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/svm/hyper/svmhyper3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/svm/hyper/svmhyper4.png')

        
        elif model == 'LGBM':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/lgbm/hyper/lgbmhyper1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/lgbm/hyper/lgbmhyper2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/lgbm/hyper/lgbmhyper3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/lgbm/hyper/lgbmhyper4.png')
        

        elif model == 'Random Forest':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/rb/hyper/rbhyper1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/rb/hyper/rbhyper2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/rb/hyper/rbhyper3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/rb/hyper/rbhyper4.png')
        
        elif model == 'xg':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/xg/hyper/xghyper1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/xg/hyper/xghyper2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/xg/hyper/xghyper3.png')
            with col4:
                st.markdown('#####  Learning Curve')
                st.image('./data/results/xg/hyper/xghyper4.png')
                
                

# 22년도 데이터 검증
def test22(model):
        if model == 'Logistic Regression':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/logi/testresult/logitest1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/logi/testresult/logitest2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/logi/testresult/logitest3.png')
            with col4:
                st.markdown('##### Accuracy')
                st.markdown('### 점수: 72.43점')
        
        elif model == 'SVM':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/svm/testresult/svmtest1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/svm/testresult/svmtest2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/svm/testresult/svmtest3.png')
            with col4:
                st.markdown('##### Accuracy')
                st.markdown('### 점수: 73.41점')

        
        elif model == 'LGBM':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/lgbm/testresult/lgbmtest1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/lgbm/testresult/lgbmtest2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/lgbm/testresult/lgbmtest3.png')
            with col4:
                st.markdown('##### Accuracy')
                st.markdown('### 점수: 61.76점')
        

        elif model == 'Random Forest':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/rb/testresult/rbtest1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/rb/testresult/rbtest2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/rb/testresult/rbtest3.png')
            with col4:
                st.markdown('##### Accuracy')
                st.markdown('### 점수: 72.00점')
        
        elif model == 'xg':
            col1, col2 = st.columns(2)
            with col1:
                st.markdown('##### Confusion Matrix')
                st.image('./data/results/xg/testresult/xgtest1.png')
            with col2:
                st.markdown('##### Classification Report')
                st.image('./data/results/xg/testresult/xgtest2.png')
            col3,col4 = st.columns(2)
            with col3:
                st.markdown('#####  ROC Curve')
                st.image('./data/results/xg/testresult/xgtest3.png')
            with col4:
                st.markdown('##### Accuracy')
                st.markdown('### 점수: 61.27점')
                