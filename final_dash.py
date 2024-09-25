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
        - 허리둘레: {profile_info['허리둘레']} cm/{round(float(profile_info['허리둘레'])/2.54,2)} 인치
        
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
        if profile_pdf['신체정보']['성별'] == '남성':
            fig_whtr.update_layout(
                title='WhtR (허리둘레-신장 비율)',
                height=150,
                width=300,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(
                    autorange=True,  # 오토스케일 적용
                    tickvals=[0, 0.43, 0.50, 0.58, 0.63],
                    ticktext=['0', '0.43', '0.50', '0.58', '0.63'],
                    title='WhtR 값'
                ),
                yaxis=dict(showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
        else:
            fig_whtr.update_layout(
                title='WhtR (허리둘레-신장 비율)',
                height=150,
                width=300,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(
                    autorange=True,  # 오토스케일 적용
                    tickvals=[0, 0.42, 0.47, 0.54, 0.59],
                    ticktext=['0', '0.42', '0.47', '0.54', '0.59'],
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
        
        # 상위 % 계산 함수
        def calculate_rank(df, column, profile_value):
                rank = (df[column] < profile_value).mean() * 100
                return 100 - rank  # 상위 % 반환
            
        user_age = int(profile_pdf['신체정보']['만 나이'])
        user_gender = profile_pdf['신체정보']['성별']
        
        data_df = pd.read_csv('./data/csv/pridicted_df.csv')
        filtered_df = data_df[(data_df['만나이'] >= (user_age - 10)) & (data_df['만나이'] <= (user_age + 10)) & 
                                (data_df['성별'] == (1 if user_gender == "남성" else 2) )]
        
        def plot_distribution(df, column, profile_value, title, profile_rank):
            # 데이터 백분위 계산 (상위 100%에서 하위 0%로)
            percentiles = np.percentile(df[column], np.arange(0, 101, 1))
            # profile_value에 해당하는 백분위 계산 (상위 %)
            profile_percentile = np.searchsorted(percentiles, profile_value)  # 상위 % 기준으로 계산
            # 바 차트 생성
            fig = go.Figure()
            # 배경 바 추가 (100% 기준)
            fig.add_trace(go.Bar(
                y=[column],
                x=[100],  # 100%로 설정
                orientation='h',
                marker=dict(color='rgba(0,0,0,0.1)'),
                hoverinfo='none',
                showlegend=False
            ))
            # 실제 값에 해당하는 백분위 값 추가
            fig.add_trace(go.Bar(
                y=[column],
                x=[profile_percentile],  # 상위 %를 기준으로 설정
                orientation='h',
                marker=dict(color='rgba(0,0,0,0.8)'),
                hoverinfo='none',
                showlegend=False
            ))

            colors = ['#ffcccc', '#ff6666', '#ff3333', '#cc0000']  # 연한 빨간색 -> 진한 빨간색 그라데이션
            ranges = [100, 75, 50, 25, 0]  # 상위 % 구간 설정
                
            for i in range(len(colors)):
                fig.add_shape(
                    type='rect',
                    x0=ranges[i+1],  # 하위 % 범위 설정
                    x1=ranges[i],
                    y0=0,
                    y1=1,
                    yref='paper',
                    fillcolor=colors[i],
                    opacity=0.3,
                    layer='below',
                    line_width=0
                )
            # profile_value 값과 상위 % 표시
            fig.add_annotation(
                x=profile_percentile,  # 상위 % 위치에 주석 추가
                y=1,
                text=f'상위 {profile_rank:.2f}%',  # 퍼센트값 표시
                showarrow=True,
                arrowhead=2,
                yshift=10
            )
            # 그래프 레이아웃 설정
            fig.update_layout(
                title=title,
                height=150,
                width=400,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(
                    autorange=True,  # 오토스케일 해제
                    range=[0, 100],  # 100에서 0까지
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['100%', '75%', '50%', '25%', '0%'],
                    title="상위 백분위 (%)"
                ),
                yaxis=dict(showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig)
            return fig
        def plot_distribution2(df, column, profile_value, title, profile_rank):
            # 데이터 백분위 계산 (상위 100%에서 하위 0%로)
            percentiles = np.percentile(df[column], np.arange(0, 101, 1))
            # profile_value에 해당하는 백분위 계산 (상위 %)
            profile_percentile = 100 - np.searchsorted(percentiles, profile_value)  # 상위 % 기준으로 계산
            # 바 차트 생성
            fig = go.Figure()
            # 배경 바 추가 (100% 기준)
            fig.add_trace(go.Bar(
                y=[column],
                x=[100],  # 100%로 설정
                orientation='h',
                marker=dict(color='rgba(0,0,0,0.1)'),
                hoverinfo='none',
                showlegend=False
            ))
            # 실제 값에 해당하는 백분위 값 추가
            fig.add_trace(go.Bar(
                y=[column],
                x=[profile_percentile],  # 상위 %를 기준으로 설정
                orientation='h',
                marker=dict(color='rgba(0,0,0,0.8)'),
                hoverinfo='none',
                showlegend=False
            ))


            colors = ['#cc0000','#ff3333', '#ff6666', '#ffcccc']  # 연한 빨간색 -> 진한 빨간색 그라데이션
            ranges = [100, 75, 50, 25, 0]  # 상위 % 구간 설정     


            for i in range(len(colors)):
                fig.add_shape(
                    type='rect',
                    x0=ranges[i+1],  # 하위 % 범위 설정
                    x1=ranges[i],
                    y0=0,
                    y1=1,
                    yref='paper',
                    fillcolor=colors[i],
                    opacity=0.3,
                    layer='below',
                    line_width=0
                )
            # profile_value 값과 상위 % 표시
            fig.add_annotation(
                x=profile_percentile,  # 상위 % 위치에 주석 추가
                y=1,
                text=f'상위 {profile_rank:.2f}%',  # 퍼센트값 표시
                showarrow=True,
                arrowhead=2,
                yshift=10
            )
            # 그래프 레이아웃 설정
            fig.update_layout(
                title=title,
                height=150,
                width=400,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(
                    autorange=True,  # 오토스케일 해제
                    range=[0, 100],  # 100에서 0까지
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['0%', '25%', '50%', '75%', '100%'],
                    title="상위 백분위 (%)"
                ),
                yaxis=dict(showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig)
            return fig

        def plot_distribution3(df, column, profile_value, title, profile_rank):
            # 데이터 백분위 계산 (상위 100%에서 하위 0%로)
            percentiles = np.percentile(df[column], np.arange(0, 101, 1))
            # profile_value에 해당하는 백분위 계산 (상위 %)
            profile_percentile = np.searchsorted(percentiles, profile_value)  # 상위 % 기준으로 계산
            # 바 차트 생성
            fig = go.Figure()
            # 배경 바 추가 (100% 기준)
            fig.add_trace(go.Bar(
                y=[column],
                x=[100],  # 100%로 설정
                orientation='h',
                marker=dict(color='rgba(0,0,0,0.1)'),
                hoverinfo='none',
                showlegend=False
            ))
            # 실제 값에 해당하는 백분위 값 추가
            fig.add_trace(go.Bar(
                y=[column],
                x=[profile_percentile],  # 상위 %를 기준으로 설정
                orientation='h',
                marker=dict(color='rgba(0,0,0,0.8)'),
                hoverinfo='none',
                showlegend=False
            ))

            colors = ['#cc0000','#ff3333', '#ff6666', '#ffcccc']  # 연한 빨간색 -> 진한 빨간색 그라데이션
            ranges = [100, 75, 50, 25, 0]  # 상위 % 구간 설정  
                


            for i in range(len(colors)):
                fig.add_shape(
                    type='rect',
                    x0=ranges[i+1],  # 하위 % 범위 설정
                    x1=ranges[i],
                    y0=0,
                    y1=1,
                    yref='paper',
                    fillcolor=colors[i],
                    opacity=0.3,
                    layer='below',
                    line_width=0
                )
            # profile_value 값과 상위 % 표시
            fig.add_annotation(
                x=profile_percentile,  # 상위 % 위치에 주석 추가
                y=1,
                text=f'상위 {profile_rank:.2f}%',  # 퍼센트값 표시
                showarrow=True,
                arrowhead=2,
                yshift=10
            )
            # 그래프 레이아웃 설정
            fig.update_layout(
                title=title,
                height=150,
                width=400,
                margin=dict(l=0, r=0, t=30, b=0),
                xaxis=dict(
                    autorange=True,  # 오토스케일 해제
                    range=[0, 100],  # 100에서 0까지
                    tickvals=[0, 25, 50, 75, 100],
                    ticktext=['0%', '75%', '50%', '25%', '0%'],
                    title="상위 백분위 (%)"
                ),
                yaxis=dict(showticklabels=False),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )

            st.plotly_chart(fig)
            return fig



        physical_activity_rank = calculate_rank(filtered_df, '신체활동점수', act_score)                
        physical_activity_rank = round(physical_activity_rank,2)
        plot_distribution(filtered_df, '신체활동점수', act_score, "신체활동 점수", physical_activity_rank)
        
        
        alcohol_score_rank = calculate_rank(filtered_df, '음주 점수', int(profile_score['음주 점수']))
        plot_distribution2(filtered_df, '음주 점수', int(profile_score['음주 점수']), "음주 점수", alcohol_score_rank)        
        
        hypertension_rank = calculate_rank(filtered_df, '고혈압 확률', float(profile_score['고혈압 확률']))
        hypertension_rank = round(hypertension_rank,2)
        plot_distribution3(filtered_df, '고혈압 확률', float(profile_score['고혈압 확률']), "고혈압 확률", hypertension_rank)
        
    with big_c:

        
        # cm 
        ideal_waist = cal_waist_ideal(round(float(profile_pdf['신체정보']['키']),2), profile_pdf['신체정보']['성별'], False)
        # 인치
        ideal_waist2 = cal_waist_ideal( round(float(profile_pdf['신체정보']['키']),2), profile_pdf['신체정보']['성별'],True)

        # st.markdown(f'''
        #             <div style="border: 2px solid rgba(0,0,0,0.1); border-radius: 10px; padding: 10px; width: 300px;">
        #             <span style="font-weight: bold; ">{profile_pdf['신체정보']['이름']}</span>님의 이상적인 허리둘레는 약 
        #             <span style="font-weight: bold; ">{round(ideal_waist['waist_min'],2)} cm</span> ~ 
        #             <span style="font-weight: bold; ">{round(ideal_waist['waist_max'],2)} cm</span>입니다.<br> 
        #             인치로는 약 
        #             <span style="font-weight: bold; ">{round(ideal_waist2['waist_min'],2)} 인치</span> ~ 
        #             <span style="font-weight: bold; ">{round(ideal_waist2['waist_max'],2)} 인치</span>입니다.<br>
        #             </div>
        #             ''', unsafe_allow_html=True)
             
        st.markdown('#### 종합평가')
        def words_for_person(name,
                             height,
                             waist,
                             al_score,
                             act_score,
                             hypertension_proba,
                             hypertension_rank,
                             physical_activity_rank,
                             waist_min,
                             waist_max,
                             waist_min2,
                             waist_max2
                             ):
            
            words = f'''
            {name}님의 설문에 대한 종합 평가는 다음과 같습니다.
            '''
            if hypertension_proba != None:
                words += f'\n- 모델의 결과로는 **{hypertension_proba}%** 의 확률로 고혈압 위험이 있으며,'
            if hypertension_rank != None:
                words += f' {name}님과 비슷한 사람들의 군집은 **{len(filtered_df)}** 명입니다. '
                if hypertension_rank < 10:
                    words += f' 이 중에서 고혈압 확률은 상위 **{hypertension_rank}%** 입니다. 고혈압에 필히 주의가 필요합니다.'
                elif hypertension_rank < 30:
                    words += f' 이 중에서 고혈압 확률은 상위 **{hypertension_rank}%** 입니다. 고혈압에 주의가 필요할수도 있어요.'
                elif hypertension_rank < 50:
                    words += f' 이 중에서 고혈압 확률은 상위 **{hypertension_rank}%** 입니다. 고혈압에 주의가 필요해요.'
                elif hypertension_rank < 70:
                    words += f' 이 중에서 고혈압 확률은 상위 **{hypertension_rank}%** 입니다. 나름 건강하신 상태 입니다.'
                else:
                    words += f' 이 중에서 고혈압 확률은 상위 **{hypertension_rank}%** 입니다. 매우 건강하신 상태입니다.'
            
            
            if al_score != None:
                words += f'\n- 음주 점수는 **{al_score}** 점으로,'
                if al_score < 10:
                    words += f' 음주 점수가 낮은편 입니다.'
                elif al_score < 20:
                    words += f' 음주 점수가 다소 낮은편 입니다.'
                elif al_score < 30:
                    words += f' 음주 점수가 살짝 높습니다.'
                elif al_score < 35:
                    words += f' 음주 점수가 매우 높아요.'
                else:
                    words += f' 음주를 꼭 줄이셔야 합니다.'
            
            
            if act_score != None:
                words += f'\n- 신체활동 점수는 **{act_score}** 점으로, **{len(filtered_df)}명** 의 사람들 중에서 상위 **{physical_activity_rank}%** 입니다.'
                if act_score >= -1 and act_score <= 2:
                    words += f' 신체활동 점수가 낮은편으로 신체활동량을 늘리는 것을 추천합니다.'
                elif act_score > 2 and act_score <= 4:
                    words += f' 신체활동 점수가 평범한 편으로 신체활동량을 늘리는 것을 추천합니다.'
                elif act_score > 4 and act_score <= 6:
                    words += f' 신체활동 점수가 높은 편으로 신체활동을 꾸준히 하시고 있습니다.'
                elif act_score > 6 and act_score <= 8:
                    words += f' 신체활동 점수가 매우 높습니다. 신체활동을 꾸준히 하시고 있습니다.'
                elif act_score > 8:
                    words += f' 혹시 운동 선수 이신가요?'
                    
            if height != None:
                words += f'''\n- {name}님의 신장인 **{height} cm** 에서 이상적인 허리둘레는 **{waist_min} cm** ~ **{waist_max} cm** 입니다.
                인치로는 **{waist_min2} 인치** ~ **{waist_max2} 인치** 입니다.
                '''
                if waist_min <= waist <= waist_max:
                    words += f' 허리둘레가 이상적인 범위 안에 있어요.'
                if waist < waist_min:
                    words += f' 허리둘레가 약 **{waist_min - waist} cm** 벗어났습니다.(약 **{round((waist_min - waist)/2.54,2)}** 인치)'
                if waist > waist_max:
                    words += f' 허리둘레가 약 **{waist - waist_max} cm** 줄여야합니다.(약 **{round((waist - waist_max)/2.54,2)}** 인치)'
    
            return words
        st.markdown(words_for_person(profile_pdf['신체정보']['이름'],
                         float(profile_pdf['신체정보']['키']),
                         float(profile_pdf['신체정보']['허리둘레']),
                         int(profile_score['음주 점수']),
                         round(float(profile_score['신체활동 점수']),2),
                         float(profile_score['고혈압 확률']),
                         round(hypertension_rank,2),
                         round(physical_activity_rank,2),
                         round(ideal_waist['waist_min'],2),
                         round(ideal_waist['waist_max'],2),
                         round(ideal_waist2['waist_min'],2),
                         round(ideal_waist2['waist_max'],2)
                         ))
                             
                             
            
            


