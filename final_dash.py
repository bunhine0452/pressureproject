import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import numpy as np
from funcs import cal_waist_ideal, linegaro ,linesero 

def final_dash():
    if 'profile_pdf' not in st.session_state:
        st.error("프로필 정보가 없습니다. 먼저 설문을 완료해 주세요.")
        return

    profile_pdf = st.session_state['profile_pdf']
    # 이름 저장
    name = profile_pdf['신체정보']['이름']
    
    act_score = float(profile_pdf['점수 및 확률 정보']['신체활동 점수'])
    
    
    st.markdown(f"# {profile_pdf['신체정보']['이름']} 님의 건강 대시보드")
    linegaro()
    big_a , big_b , big_c = st.columns([1,1,1])
    with big_a:
        # 기본 정보 섹션
        profile_info = profile_pdf['신체정보']
        st.markdown(f"""
        <div style="border: 2px solid rgba(0,0,0,0.1); border-radius: 10px; padding: 10px; width: 300px;">
        - 만 나이: {profile_info['만 나이']}세<br>
        - 성별: {profile_info['성별']}<br>
        - 신장: {profile_info['키']}cm<br>
        - 체중: {profile_info['체중']}kg<br>
        - 허리둘레: {profile_info['허리둘레']} cm/{float(profile_info['허리둘레'])/2.54} 인치
        
        </div>
        """, unsafe_allow_html=True)
        st.write('')  
        profile_info2 = profile_pdf['질병 정보']
        profile_info3 = profile_pdf['음주 관련 정보']
        profile_info4 = profile_pdf['고강도 운동 관련 정보']
        profile_info5 = profile_pdf['중강도 운동 관련 정보']
        profile_info6 = profile_pdf['걷기/자전거 관련 정보']
        profile_score = profile_pdf['점수 및 확률 정보']
        st.markdown(f"""
        <div style="border: 2px solid rgba(0,0,0,0.1); border-radius: 10px; padding: 10px; width: 300px;">
        - 당뇨병 여부: {profile_info2['당뇨병 여부']}<br>
        - 이상지질혈증 여부: {profile_info2['이상지질혈증 여부']}<br>
        - 음주 점수: {int(profile_score['음주 점수'])}점<br>
        - 신체활동 점수: {round(float(profile_score['신체활동 점수']),2)}점<br>
        - 고혈압 확률: {round(float(profile_score['고혈압 확률']),2)}%<br>
        </div>
        """, unsafe_allow_html=True) 
    
    with big_b:
        # cm 
        ideal_waist = cal_waist_ideal(round(float(profile_pdf['신체정보']['키']),2), '남자', False)
        # 인치
        ideal_waist2 = cal_waist_ideal( round(float(profile_pdf['신체정보']['키']),2), '남자',True)
        
        # WhtR 계산 및 표시
        height_m = float(profile_pdf['신체정보']['키'].replace('cm', ''))
        waist = float(profile_pdf['신체정보']['허리둘레'].replace('cm', ''))
        whtr = waist / height_m
        
        # WhtR 바 차트 생성
        fig_whtr = go.Figure()
        
        # 배경 바 추가
        fig_whtr.add_trace(go.Bar(
            y=['WhtR'],
            x=[0.63],
            orientation='h',
            marker=dict(color='rgba(0,0,0,0.1)'),
            hoverinfo='none',
            showlegend=False
        ))
        
        # 실제 WhtR 값을 나타내는 바 추가
        fig_whtr.add_trace(go.Bar(
            y=['WhtR'],
            x=[whtr],
            orientation='h',
            marker=dict(color='rgba(0,0,0,0.8)'),
            hoverinfo='none',
            showlegend=False
        ))
        # 레이아웃 설정
        fig_whtr.update_layout(
            title='WhtR (허리둘레-신장 비율)',
            height=150,
            width=300,
            margin=dict(l=0, r=0, t=30, b=0),
            xaxis=dict(
                range=[0, 0.63],
                tickvals=[0, 0.43, 0.53, 0.58, 0.63],
                ticktext=['0', '0.43', '0.53', '0.58', '0.63'],
                title='WhtR 값'
            ),
            yaxis=dict(showticklabels=False),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        # 색상 구간 추가
        colors = ['#50a7d9', '#77dd77', '#f8e47e', '#ed7777']
        if profile_pdf['신체정보']['성별'] == '남성':
            ranges = [0,0.43, 0.50, 0.58, 0.68]
        else:
            ranges = [0,0.42, 0.47, 0.59, 0.64]
        
        for i in range(len(colors)):
            fig_whtr.add_shape(
                type='rect',
                x0=ranges[i],
                x1=ranges[i+1],
                y0=0,
                y1=1,
                yref='paper',
                fillcolor=colors[i],
                opacity=0.3,
                layer='below',
                line_width=0
            )
        # WhtR 값 표시
        fig_whtr.add_annotation(
            x=whtr,
            y=1,
            text=f'WhtR: {whtr:.2f}',
            showarrow=True,
            arrowhead=2,
            yshift=10
        )
        st.plotly_chart(fig_whtr)
        st.markdown(f'''
                    <div style="border: 2px solid rgba(0,0,0,0.1); border-radius: 10px; padding: 10px; width: 300px;">
                    <span style="font-weight: bold; ">{profile_pdf['신체정보']['이름']}</span>님의 이상적인 허리둘레는 약 
                    <span style="font-weight: bold; ">{round(ideal_waist['waist_min'],2)} cm</span> ~ 
                    <span style="font-weight: bold; ">{round(ideal_waist['waist_max'],2)} cm</span>입니다.<br> 
                    인치로는 약 
                    <span style="font-weight: bold; ">{round(ideal_waist2['waist_min'],2)} 인치</span> ~ 
                    <span style="font-weight: bold; ">{round(ideal_waist2['waist_max'],2)} 인치</span>입니다.<br>
                    </div>
                    ''', unsafe_allow_html=True)
    
    with big_c:
        def calculate_rank(df, column, profile_value):
                rank = (df[column] < profile_value).mean() * 100
                return 100 - rank  # 상위 % 반환
        def calculate_mean(df, column):
                return df[column].mean()
            
        user_age = int(profile_pdf['신체정보']['만 나이'])
        user_gender = profile_pdf['신체정보']['성별']
        
        data_df = pd.read_csv('./data/csv/pridicted_df.csv')
        filtered_df = data_df[(data_df['만나이'] >= (user_age - 10)) & (data_df['만나이'] <= (user_age + 10)) & 
                                (data_df['성별'] == (1 if user_gender == "남성" else 2) )]
        
        physical_activity_rank = calculate_rank(filtered_df, '신체활동점수', act_score)                
        physical_activity_rank = round(physical_activity_rank,2)
        st.markdown(f'{name}님과 비슷한 사람들은 약{len(filtered_df)}명의 사람들이 있습니다.{physical_activity_rank}')
        st.markdown('종합평가')
        def words_for_person(name,weight,waist,al_score,act_score,hypertension_proba):
            
            words = f'''
            {name}님의 종합평가는 다음과 같습니다.
            '''
            if hypertension_proba != None:
                words += f'모델의 결과로는 **{hypertension_proba}%** 의 확률로 고혈압 위험이 있습니다.'
            if al_score > 10:
                words += f'음주 점수는 {al_score}점으로, 적절한 음주 습관이 필요합니다.'
            if act_score < 5:
                words += f'신체활동 점수는 {act_score}점으로, 더 적극적인 신체활동이 필요합니다.'
            return words
        st.markdown(words_for_person(profile_pdf['신체정보']['이름'],
                         profile_pdf['신체정보']['체중'],
                         profile_pdf['신체정보']['허리둘레'],
                         float(profile_score['음주 점수']),
                         float(profile_score['신체활동 점수']),
                         float(profile_score['고혈압 확률'])))
                             
                             
            
            


