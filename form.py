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


def form_page():
    st.sidebar.markdown(
        """
        <div style="border-top: 3px solid #3F5277; width: 100%;"></div>
        """,
        unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 18px; color:rgba(246,244,241,1);"> 🦥 설문을 통해 나의 건강상태와 고혈압 예측을 해보실 수 있습니다. </p>', unsafe_allow_html=True)
    st.sidebar.markdown("")
    a, b = st.columns([1,7])
    with a:
        st.image('./data/image/temp_logo2-removebg-preview.png')
    with b:
        st.title('나의 고혈압 확률 예측해보기')
    linegaro()
    st.markdown('#####')
    # form 생성
    with st.form('form'):
        a,b,c,d = st.columns(4)
        with a:
            name = st.text_input('이름을 입력하세요:')
        with b:
            # 숫자 입력 받기
            age = st.number_input('만 나이를 입력하세요:', min_value=18, max_value=79,help='만나이18~79세 까지만 입력하실수 있습니다.')
        with c:
            gender = st.radio('성별을 선택하세요:', ('남성', '여성'))
        
        a,b,c,d = st.columns(4)
        with a:
            # 선택 박스 사용
            height = st.number_input('키를 입력해주세요(cm)')
        with b:
            weight = st.number_input('몸무게를 입력해주세요')
        with c:
            waist = st.number_input('허리들레를 입력해주세요')
            if st.checkbox('인지로 입력'):
                waist *= 2.54
        linegaro()
        st.markdown('##### 질병 관련 설문')
        a,b,c = st.columns(3)
        with a:
            disease1 = st.radio('당뇨병 유병여부', ('있다', '없다'))
        with b:
            disease2 = st.radio('고지혈증,고콜레스테롤혈증 유병여부', ('있다', '없다'),help="둘 중에 하나라도 해당할 경우 '있다' 라고 해주세요")
        linegaro()

        # 음주 관련 설문        
        st.markdown('##### 음주 관련 설문')
        a,b,c,d = st.columns(4)
        with a:
            ever_al = st.radio('나는 술을',('마신다','마시지 않는다'),help='*마시지 않을 경우 신체활동 설문으로 이동*')
        
        a,b,c = st.columns(3)
        with a:
            how_al = st.radio("술을 얼마나 자주 마십니까?", 
                                           ("최근 1년간 전혀 마시지 않았다.", "월1회미만", "월1회정도", "월2~4회", "주2~3회 정도", "주 4회 이상"))
        with b:     
            ones_al = st.radio("한번에 술을 얼마나 마십니까?", 
                                                    ("0-2잔", "3-4잔", "5-6잔", "7-9잔", "10잔 이상"))
        a,b,c = st.columns(3)
        with a:
            wasted_al = st.selectbox("한 번의 술자리에서 7잔 이상을 마시는 횟수는?", 
                                                    ("전혀 없음", "월 1회 미만", "월 1회 정도", "주 1회 정도", "거의 매일"))
        with b:
            stop_al = st.selectbox("술을 끊거나 줄이라는 권고를 받은 적이 있습니까?", 
                                                    ("없음", "가족/의사 권고", "가족/의사 강력 권고"))
        with c:
            therapy_al = st.selectbox("최근 1년 동안 음주문제로 상담을 받아본 적이 있습니까?", 
                                                    ("없음", "있음"))
        linegaro()     
        
        # 신체활동 관련 설문
        st.markdown('##### 신체활동 관련 설문')

        a, b, c = st.columns(3)
        with a:
            st.markdown("##### 고강도 운동 관련 설문")
            high_do = st.radio("고강도 운동을 하십니까?", ("안 한다", "한다"))
            st.write("###### 근력운동을 동반한 무산소운동, 신체에 과부화를 아주 많이 주는 행위를 일컫습니다.")
            high_days = st.select_slider("일주일에 고강도 운동 (일 수)",options=range(1,8),value=1)
            col1,col2 = st.columns(2)
            with col1:
                high_hour = st.number_input("고강도 운동 시간") 
            with col2:
                high_min = st.number_input("고강도 운동 분")
        with b:
            st.markdown("##### 중강도 운동 관련 설문")
            mid_do = st.radio("중강도 운동을 하십니까?", ("안 한다", "한다"))
            st.write("###### 고강도 운동만큼은 아니지만 유산소를 제외한 신체에 과부화를 주는 행위를 일컫습니다.")
            mid_days = st.select_slider("일주일에 중강도 운동 (일 수)",options=range(1,8),value=1)
            col1,col2 = st.columns(2)
            with col1:
                mid_hour = st.number_input("중강도 운동 시간") 
            with col2:
                mid_min = st.number_input("중강도 운동 분")
        with c:
            st.markdown("##### 유산소 운동 관련 설문")
            walk_do = st.radio("유산소 행위를 하십니까?", ("안 한다", "한다"))
            st.write("###### 산책 또는 가벼운 운동 그리고 통근시간에 걷는 시간을 입력해주시면 됩니다.")
            walk_days = st.select_slider("일주일에 유산소 운동 (일 수)",options=range(1,8),value=1)
            col1,col2 = st.columns(2)
            with col1:
                walk_hour = st.number_input("유산소 운동 시간") 
            with col2:
                walk_min = st.number_input("유산소 운동 분")
        # 제출 버튼 생성
        st.markdown('######')
        submitted = st.form_submit_button('제출')

    # 제출이 완료되면 결과 출력
    if submitted:
        alcohol_score = calculate_alcohol_score(ever_al,how_al,ones_al,wasted_al,stop_al,therapy_al)
        physical_activity_score = calculate_physical_activity_score(high_do,high_days,high_hour,high_min,mid_do,mid_days,mid_hour,mid_min,walk_do,walk_days,walk_hour,walk_min)
        whtR_category = calculate_whtR_category(gender,waist,height)
        if gender == '여성':
            alcohol_score = 2*alcohol_score 
            physical_activity_score = round(np.log1p(2*physical_activity_score),5)
        else:
            alcohol_score = alcohol_score
            physical_activity_score = round(np.log1p(physical_activity_score),5)
                
        # 예측을 돌릴 프로필
        profile_data = {
            '만나이':age,
            '체중': weight,
            '음주 점수': alcohol_score,
            '신체활동점수': physical_activity_score,
            'WHtR_category': whtR_category,
            '성별': 1 if gender == "남자" else 2,
            '이상지질혈증 여부': 1 if disease1 == "있음" else 0,
            '당뇨병 유병여부(19세이상)': 1 if disease2 == "있음" else 0
        }
        profile_to_predict= pd.DataFrame([profile_data]) 

        preprocessor = joblib.load('./data/model/preprocessor.pkl')  # 전처리기 로드                
        profile_transformed = preprocessor.transform(profile_to_predict)
        model = joblib.load('./data/model/hypertension_model.pkl')
        predicted_proba = model.predict_proba(profile_transformed)
        hypertension_proba = predicted_proba[0][1]  # 두 번째 클래스(고혈압)의 확률
        # 보여줄 프로필
        a,b = st.columns(2)
        with a:
            st.markdown(f'#### {name}님의 고혈압 확률은 {round(hypertension_proba * 100, 2)}% 입니다.')
            profile_pdf = {
                        "신체정보": {
                            "이름": name,
                            "만 나이": f'{age} 세',
                            "성별": gender,
                            "키": f'{height}cm',
                            "체중": f'{weight}kg',
                            "허리둘레": f'{waist}cm',
                        },
                        "질병 정보": {
                            "이상지질혈증 여부": disease1,
                            "당뇨병 여부": disease2
                        },
                        "음주 관련 정보": {
                            "술을 마십니까?": ever_al,
                            "술을 얼마나 자주 마십니까?": how_al if ever_al == "마신다" else None,
                            "한 번에 술을 얼마나 마십니까?": ones_al if ever_al == "마신다" else None,
                            "한 번의 술자리에서 7잔 이상을 마시는 횟수": wasted_al if ever_al == "마신다" else None,
                            "술을 끊거나 줄이라는 권고를 받은 적이 있습니까?": stop_al if ever_al == "마신다" else None,
                            "최근 1년 동안 음주 문제로 상담을 받아본 적이 있습니까?": therapy_al if ever_al == "마신다" else None
                        },
                        "고강도 운동 관련 정보": {
                            "고강도 운동 여부": high_do,
                            "1주일에 며칠 하십니까?": f'{high_days}일' if high_do == "한다" else None,
                            "한 번 할 때 몇 시간 하십니까?": f"{high_hour}시간 {high_min}분" if high_do == "한다" else None
                        },
                        "중강도 운동 관련 정보": {
                            "중강도 운동 여부": mid_do,
                            "1주일에 며칠 하십니까?": f'{mid_days}일' if mid_do == "한다" else None,
                            "한 번 할 때 몇 시간 하십니까?": f"{mid_hour}시간 {mid_min}분" if mid_do == "한다" else None
                        },
                        "걷기/자전거 관련 정보": {
                            "걷기나 자전거를 이용하십니까?": walk_do,
                            "1주일에 며칠 하십니까?": f'{walk_days} 일' if walk_do == "한다" else None,
                            "(하루) 대략 몇 시간 움직이십니까?": f"{walk_hour}시간 {walk_min}분" if walk_do == "한다" else None
                        },
                        # 음주 점수, 신체활동 점수, 고혈압 확률 추가
                        "점수 및 확률 정보": {
                            "음주 점수": f'{alcohol_score} 점',
                            "신체활동 점수": f'{physical_activity_score} 점',  
                            "고혈압 확률": f'{round(hypertension_proba * 100, 2)}%'  # 고혈압 확률
                        }
                    }
            st.json(profile_pdf)
            
        with b:
            # 상위 % 계산 함수
            def calculate_rank(df, column, profile_value):
                rank = (df[column] < profile_value).mean() * 100
                return 100 - rank  # 상위 % 반환
            def calculate_mean(df, column):
                return df[column].mean()
            # 그래프를 그리는 함수
            def plot_distribution(df, column, profile_value, title, profile_rank):
                fig = px.histogram(df, x=column, nbins=20, title=title, color_discrete_sequence=['#FF6699'], opacity=0.75)
                
                # 사용자 결과 값 표시 (세로선)
                fig.add_vline(x=profile_value, line_dash="dash", line_color="red", 
                            annotation_text=f"{name}님의 결과 (상위 {profile_rank:.2f}%)", annotation_position="top right")
                # 그래프 레이아웃 조정
                fig.update_layout(
                    title={'text': title, 'x': 0.5, 'xanchor': 'center'},  # 타이틀 가운데 정렬
                    xaxis_title=column,
                    yaxis_title="인원수",
                    template="plotly_white",
                    height=300,
                    width=600,
                    plot_bgcolor='rgba(0, 0, 0, 0)', 
                    paper_bgcolor='rgba(0, 0, 0, 0)'
                )
                st.plotly_chart(fig)
                return fig
            # 사용자 나이대 및 성별 필터링
            user_age = age
            user_gender = gender

            # 예시 데이터 로드 및 필터링
            data_df = pd.read_csv('./data/csv/pridicted_df.csv')
            filtered_df = data_df[(data_df['만나이'] >= (user_age - 5)) & (data_df['만나이'] <= (user_age + 5)) & 
                                (data_df['성별'] == (1 if user_gender == "남자" else 2))]

            st.markdown(f'####  {name}님의 나이대 {user_age - 5}세 ~ {user_age + 5}세 속 분포 위치')

            # 신체활동 점수 상위 % 계산 및 그래프
            profile_physical_activity_score = physical_activity_score
            physical_activity_rank = calculate_rank(filtered_df, '신체활동점수', profile_physical_activity_score)                
            plot_distribution(filtered_df, '신체활동점수', profile_physical_activity_score, "신체활동 점수 분포", physical_activity_rank)
            physical_activity_rank = round(physical_activity_rank,2)
            physical_activity_mean = calculate_mean(filtered_df, '신체활동점수')
            physical_activity_mean = round(physical_activity_mean,2)
            
            st.markdown(f"""
            동나이대, 성별의 평균 신체활동 점수는: <span style="color:#7498bf;">{physical_activity_mean}점</span> 입니다.
            <span style="color:#ed7a9e;">{name}</span>님의 신체활동 점수는 <span style="color:#ed7a9e;">{round(physical_activity_score,2)}점</span> 입니다.
            """, unsafe_allow_html=True)

            if physical_activity_rank < 20:
                st.markdown(f'상위<span style="color:#ed7a9e;">{physical_activity_rank}%</span>로 동나이대, 성별 대비 매우 활동적이시네요!', unsafe_allow_html=True)
            elif physical_activity_rank < 40:
                st.markdown(f'상위<span style="color:#ed7a9e;">{physical_activity_rank}%</span>로 동나이대, 성별 대비 남들보다 더 많이 움직이시네요!', unsafe_allow_html=True)
            elif physical_activity_rank < 60:
                st.markdown(f'상위<span style="color:#ed7a9e;">{physical_activity_rank}%</span>로 동나이대, 성별 대비 남들만큼 움직이시네요!', unsafe_allow_html=True)
            elif physical_activity_rank < 80:
                st.markdown(f'상위<span style="color:#ed7a9e;">{physical_activity_rank}%</span>로 더 활동적일 필요가 있어요.', unsafe_allow_html=True)
            else:
                st.markdown(f'상위<span style="color:#ed7a9e;">{physical_activity_rank}%</span>로 더더욱 활동적일 필요가 있어요.', unsafe_allow_html=True)
            
            # 음주 점수 상위 % 계산 및 그래프
            alcohol_score_rank = calculate_rank(filtered_df, '음주 점수', alcohol_score)
            plot_distribution(filtered_df, '음주 점수', alcohol_score, "음주 점수 분포", alcohol_score_rank)
            alcohol_score_rank = round(alcohol_score_rank,2)
            alcohol_score_mean = calculate_mean(filtered_df, '음주 점수')
            alcohol_score_mean = round(alcohol_score_mean,2)
            
            st.markdown(f"""
            동나이대, 성별의 평균 음주 점수는: <span style="color:#7498bf;">{alcohol_score_mean}점</span> 입니다.
            <span style="color:#ed7a9e;">{name}</span>님의 음주 점수는 <span style="color:#ed7a9e;">{round(alcohol_score,2)}점</span> 입니다.
            """, unsafe_allow_html=True)

            if 0 < alcohol_score_rank < 20:
                st.markdown(f'상위<span style="color:#ed7a9e;">{alcohol_score_rank}%</span>로 동나이대, 성별 대비 음주 점수가 매우 높아요.', unsafe_allow_html=True)
            elif alcohol_score_rank < 40:
                st.markdown(f'상위<span style="color:#ed7a9e;">{alcohol_score_rank}%</span>로 동나이대, 성별 대비 음주 점수가 다소 높은편이에요.', unsafe_allow_html=True)
            elif alcohol_score_rank < 60:
                st.markdown(f'상위<span style="color:#ed7a9e;">{alcohol_score_rank}%</span>로 동나이대, 성별 대비 평범하세요.', unsafe_allow_html=True)
            elif alcohol_score_rank < 80:
                st.markdown(f'상위<span style="color:#ed7a9e;">{alcohol_score_rank}%</span>로 음주를 건강하게 즐기시고 있어요.', unsafe_allow_html=True)
            else:
                st.markdown(f'상위<span style="color:#ed7a9e;">{alcohol_score_rank}%</span>로 음주를 하시지 않는군요?', unsafe_allow_html=True)    
            # 고혈압 확률 상위 % 계산 및 그래프
            hypertension_proba_percent = hypertension_proba * 100
            hypertension_rank = calculate_rank(filtered_df, '고혈압 확률', hypertension_proba_percent)
            plot_distribution(filtered_df, '고혈압 확률', hypertension_proba_percent, "고혈압 확률 분포", hypertension_rank)
            hypertension_rank = round(hypertension_rank,2)
            hypertension_mean = calculate_mean(filtered_df, '고혈압 확률')
            hypertension_mean = round(hypertension_mean,2)
            
            st.markdown(f"""
                동나이대, 성별의 평균 고혈압 확률은: <span style="color:#7498bf;">{hypertension_mean}%</span> 입니다. 
                <span style="color:#ed7a9e;">{name}</span>님의 고혈압 확률은 <span style="color:#ed7a9e;">{round(hypertension_proba*100,2)}%</span> 입니다. 
                """, unsafe_allow_html=True)
            
            if hypertension_rank < 20:
                st.markdown(f'상위<span style="color:#ed7a9e;">{hypertension_rank}%</span>로 동나이대, 성별 대비 고혈압 확률이 매우 높아요. 필히 주의가 필요합니다.', unsafe_allow_html=True)
            elif hypertension_rank < 40:
                st.markdown(f'상위<span style="color:#ed7a9e;">{hypertension_rank}%</span>로 동나이대, 성별 대비 고혈압 확률이 높아요, 주의가 필요할수도 있어요.', unsafe_allow_html=True)
            elif hypertension_rank < 60:
                st.markdown(f'상위<span style="color:#ed7a9e;">{hypertension_rank}%</span>로 동나이대, 성별 대비 고혈압에 다소 주의가 필요해요.', unsafe_allow_html=True)
            elif hypertension_rank < 80:
                st.markdown(f'상위<span style="color:#ed7a9e;">{hypertension_rank}%</span>로 동나이대, 성별 대비 평범해요.', unsafe_allow_html=True)
            else:
                st.markdown(f'상위<span style="color:#ed7a9e;">{hypertension_rank}%</span>로 매우 건강한 편입니다.', unsafe_allow_html=True)

            
            font_regular = os.path.join(os.getcwd(), 'fonts', 'NanumGothic.ttf')
            font_bold = os.path.join(os.getcwd(), 'fonts', 'NanumGothicBold.ttf')
            class PDF(FPDF):
                def header(self):
                    # 배경색 설정 (페이지 전체를 덮는 사각형 그리기)
                    self.set_fill_color(255, 241, 219)  # RGB 색상: 연한 보라색 (예시)
                    self.rect(0, 0, 210, 297, 'F')  # 페이지 크기만큼 사각형 그리기 (A4: 210x297mm)
                    self.set_y(10)  # 텍스트의 y 좌표를 초기화
            # pdf 만들기
            def create_pdf(profile_pdf):
                pdf = PDF()
                pdf.add_page()

                # 한글 폰트 등록 (기본 폰트 및 굵은 폰트)
                pdf.add_font('Nanum', '', font_regular, uni=True)
                pdf.add_font('Nanum', 'B', font_bold, uni=True)  # 굵은 폰트 등록
                pdf.set_font('Nanum', '', 12)  # 기본 한글 폰트 사용

                # 신체 정보
                pdf.set_font("Nanum", 'B', 16)  # 굵은 폰트 사용
                pdf.cell(200, 8, txt=f"< {name}님의 건강 보고서 >", ln=True, align='C')
                pdf.set_font("Nanum", 'B', 12)
                pdf.cell(200, 8, txt="신체정보", ln=True)
                pdf.set_font("Nanum", '', 12)  # 다시 기본 폰트로 설정
                for key, value in profile_pdf["신체정보"].items():
                    pdf.cell(200, 8, txt=f"{key}: {value}", ln=True)

                # 질병 정보
                pdf.set_font("Nanum", 'B', 12)
                pdf.cell(200, 10, txt="질병 정보", ln=True)
                pdf.set_font("Nanum", '', 12)
                for key, value in profile_pdf["질병 정보"].items():
                    pdf.cell(200, 8, txt=f"{key}: {value}", ln=True)

                # 음주 관련 정보
                pdf.set_font("Nanum", 'B', 12)
                pdf.cell(200, 8, txt="음주 관련 정보", ln=True)
                pdf.set_font("Nanum", '', 12)
                for key, value in profile_pdf["음주 관련 정보"].items():
                    pdf.cell(200, 8, txt=f"{key}: {value}", ln=True)

                # 운동 관련 정보
                pdf.set_font("Nanum", 'B', 12)
                pdf.cell(200, 8, txt="운동 관련 정보", ln=True)
                pdf.set_font("Nanum", '', 12)
                for key, value in profile_pdf["고강도 운동 관련 정보"].items():
                    pdf.cell(200, 8, txt=f"{key}: {value}", ln=True)
                for key, value in profile_pdf["중강도 운동 관련 정보"].items():
                    pdf.cell(200, 8, txt=f"{key}: {value}", ln=True)
                for key, value in profile_pdf["걷기/자전거 관련 정보"].items():
                    pdf.cell(200, 8, txt=f"{key}: {value}", ln=True)

                # 점수 및 확률 정보
                pdf.set_font("Nanum", 'B', 12)
                pdf.cell(200, 8, txt="점수 및 확률 정보", ln=True)
                pdf.set_font("Nanum", '', 12)
                for key, value in profile_pdf["점수 및 확률 정보"].items():
                    pdf.cell(200, 8, txt=f"{key}: {value}", ln=True)
                        
                # 두 번째 페이지 추가 (그래프들 삽입)
                pdf.add_page()
                pdf.set_font("Nanum", 'B', 16)
                pdf.cell(200, 8, txt="< 나이대/성별 지표 계산 정보 >", ln=True, align='C')
                pdf.set_font("Nanum", 'B', 12)

                pdf.set_font("Nanum", 'B', 12)
                pdf.cell(200, 8, txt="음주 점수", ln=True)
                pdf.set_font("Nanum", '', 12)
                pdf.cell(200, 8, txt=f"동나이대, 성별의 평균 음주 점수는:{alcohol_score_mean}점 입니다.", ln=True)
                pdf.cell(200, 8, txt=f"{name}님의 음주 점수는{round(alcohol_score,2)}점 입니다", ln=True)
                pdf.cell(200, 8, txt=f"전체 분포에서 약 상위{alcohol_score_rank}% 입니다.", ln=True)

                pdf.set_font("Nanum", 'B', 12)
                pdf.cell(200, 8, txt="신체 활동 점수", ln=True)
                pdf.set_font("Nanum", '', 12)
                pdf.cell(200, 8, txt=f"동나이대, 성별의 평균 신체활동 점수는:{physical_activity_mean}점 입니다.", ln=True)
                pdf.cell(200, 8, txt=f"{name}님의 신체활동 점수는{round(physical_activity_score,2)}점 입니다", ln=True)
                pdf.cell(200, 8, txt=f"전체 분포에서 약 상위{physical_activity_rank}% 입니다.", ln=True)
                
                pdf.set_font("Nanum", 'B', 12)             
                pdf.cell(200, 8, txt="고혈압 확률", ln=True)
                pdf.set_font("Nanum", '', 12)
                pdf.cell(200, 8, txt=f"동나이대, 성별의 평균 고혈압 확률은:{hypertension_mean}%입니다.", ln=True)
                pdf.cell(200, 8, txt=f"{name}님의 고혈압 확률은{round(hypertension_proba*100,2)}%입니다. 전체 분포에서 약 상위{hypertension_rank}% 입니다", ln=True)
                pdf.cell(200, 8, txt=f"전체 분포에서 약 상위{hypertension_rank}% 입니다.", ln=True)

                return pdf
            # PDF 다운로드 버튼
            pdf = create_pdf(profile_pdf)

            # PDF를 BytesIO로 변환
            pdf_buffer = BytesIO()
            pdf_output = pdf.output(dest='S').encode('latin1')  # PDF 데이터를 메모리로 출력
            pdf_buffer.write(pdf_output)
            pdf_buffer.seek(0)

            # Streamlit에서 파일 다운로드
            st.download_button(label="PDF로 저장하기", data=pdf_buffer, file_name=f"{name}님 건강보고서.pdf", mime="application/pdf")