import pandas as pd
import streamlit as st
from PIL import Image
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from imblearn.over_sampling import SMOTENC

# funcs.py
from funcs import load_css, load_local_font, linegaro, linesero, csv , calculate_proportions , remove_outliers

def dashboard_page():
    st.sidebar.markdown(
        """
        <div style="border-top: 3px solid #3F5277; width: 100%;"></div>
        """,
        unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 18px; color:rgba(246,244,241,1);"> 🦥 이 페이지에선 대시보드를 통해 여러 그래프를 보실수 있습니다.</p>', unsafe_allow_html=True)
    st.sidebar.markdown("")

    a, b = st.columns([1,7])
    with a:
        st.image('./data/image/temp_logo2-removebg-preview.png')
    with b:
        st.title('국민 건강 영양조사 DATA Dashboard')
    linegaro()
    team_title = '<b style="color:#31333f; font-size: 40px;">*Data Trend*</b>'
    st.markdown(team_title, unsafe_allow_html=True)
    df1 = csv(what='train')
    df2 = csv(what='test')
    df3 = csv(what='all')
    a, b, c, d, e= st.columns(5)
    with a:
        st.markdown('##### 데이터셋 개수' ,help='Train은(19,20,21년도 데이터셋인 8기 데이터 사용) Test는(22년도 데이터셋인 9기 데이터 사용)')
        col1 ,col2 = st.columns(2)
        with col1:
            st.markdown(f"""
                <div style="margin-bottom: 5px;">
                    <span style="font-size: 18px; font-weight: bold;">Train</span>
                </div>
                <div style="margin-top: -20px;">
                    <span style="color:#beef69; font-size: 25px; font-weight: bold;">11756명</span>
                    <span style="color:#a0daa9; font-size: 13px;">전처리전:{len(df1)} 명</span>
                </div>
                
                """,unsafe_allow_html=True)
        with col2:
            st.markdown(f"""
                <div style="margin-bottom: 5px;">
                    <span style="font-size: 18px; font-weight: bold;">Test</span>
                </div>
                <div style="margin-top: -20px;">
                    <span style="color:#ed7777; font-size: 25px; font-weight: bold;">{len(df2)} 명</span>
                </div>
                """, unsafe_allow_html=True)

    with b:
        st.markdown('##### 데이터 나이 스펙트럼' ,help='성인(만19세이상)과 80미만으로 구성(80+는 분류가 되어있지 않았습니다.)')
        st.markdown(f"""
            <div style="margin-top: -10px; font-weight: bold;">
                <span style=font-size:25px; ">19세~79세</span>
            </div>
        """, unsafe_allow_html=True)
    with c:
        count_0 = df1['Target'].value_counts()[0]
        count_1 = df1['Target'].value_counts()[1]
        ratio = (count_1 / count_0)*100
        st.markdown('##### 총 고혈압환자의 비율' ,help='Train 데이터 기준 Target칼럼 속 1(고혈압 있음) 나누기 0(고혈압 없음) 사람 수를 나누었습니다.')
        st.markdown(f"""
            <div style="margin-top: -10px; font-weight: bold;">
                <span style=font-size:25px; ">{ratio:.2f}%</span>
            </div>
        """, unsafe_allow_html=True)
    with d:
        st.markdown('##### 총 사용된 칼럼 수' ,help='사용된 칼럼의: 1.만나이/2.체중/3.WhTR카테고리/4.성별/5.당뇨병유병여부/6.이상지질혈증여부/7.음주점수/8.신체활동점수')
        st.markdown(f"""
            <div style="margin-top: 10px; font-weight: bold;">
                <span style=font-size:25px; ">8개</span>
            </div>
        """, unsafe_allow_html=True)
    with e:
        st.markdown('##### 국건영 데이터 기반 추가 데이터' ,help='가지고 있는 데이터셋을 기반으로 설문칼럼 또는 신체정보를 이용해 새로운 지표를 추가했습니다.')
        st.markdown('###### *Whtr카테고리*' ,help='Whtr은 성별+신장+허리둘레로 BMI계산보다 신뢰도가 높습니다.')
        st.markdown('###### *신체 활동 점수*' ,help='고강도 운동,중강도 운동,유산소 활동에 대한 설문 칼럼을 이용하여 신체활동에 대한 지표를 나타냈습니다. 추가로 성별에 따라서 점수에 대한 계산방식을 다르게 적용했습니다.')
        st.markdown('###### *음주 점수*' ,help='음주 에 관련된 설문 칼럼을 이용해서 음주에 대한 점수화를 통해 새로운 지표를 구했습니다. 추가로 성별에 따라서 점수에 대한 계산방식을 다르게 적용했습니다.')
# 두 개의 데이터셋 로드
    df_train = csv(what='train')
    df_test = csv(what='test')
    a, b = st.columns(2)
    with a:
        pick_column = st.selectbox("칼럼별 고혈압 비율 Train vs Test 선형 그래프", 
                                    ["만 나이","체중","WHtR","허리둘레"])
        # 동일한 데이터 전처리 및 이상치 제거 적용 (train과 test 모두)
        for col in ['신장', '허리둘레', '체중', '신체활동점수']:
            df_train = remove_outliers(df_train, col)
            df_test = remove_outliers(df_test, col)

        # 음주 점수 상위 10% 제거
        threshold_train = df_train['음주 점수'].quantile(0.90)
        threshold_test = df_test['음주 점수'].quantile(0.90)

        df_train = df_train[df_train['음주 점수'] <= threshold_train]
        df_test = df_test[df_test['음주 점수'] <= threshold_test]

        # WHtR 계산 및 칼럼 추가 (train과 test 모두)
        df_train['WHtR'] = df_train['허리둘레'] / df_train['신장']
        df_test['WHtR'] = df_test['허리둘레'] / df_test['신장']

        # 비율 계산을 위한 bins 설정
        weight_bins = np.linspace(df_train['체중'].min(), df_train['체중'].max(), 10).round(1)
        waist_bins = np.linspace(df_train['허리둘레'].min(), df_train['허리둘레'].max(), 10).round(1)
        whtr_bins = np.linspace(df_train['WHtR'].min(), df_train['WHtR'].max(), 10).round(5)
        age_bins = [18, 30, 40, 50, 60, 70, 80]

        # 필요한 칼럼에 대한 비율 계산 (train과 test 모두)
        weight_dist_train = calculate_proportions(df_train, '체중', bins=weight_bins)
        weight_dist_test = calculate_proportions(df_test, '체중', bins=weight_bins)

        waist_dist_train = calculate_proportions(df_train, '허리둘레', bins=waist_bins)
        waist_dist_test = calculate_proportions(df_test, '허리둘레', bins=waist_bins)

        whtr_dist_train = calculate_proportions(df_train, 'WHtR', bins=whtr_bins)
        whtr_dist_test = calculate_proportions(df_test, 'WHtR', bins=whtr_bins)

        age_dist_train = calculate_proportions(df_train, '만나이', bins=age_bins)
        age_dist_test = calculate_proportions(df_test, '만나이', bins=age_bins)

            # 만나이에 따른 고혈압 비율 비교 (train vs test)
        if pick_column == "만 나이":
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=age_dist_test.index.astype(str), y=age_dist_test, mode='lines+markers', name='9기(22)', line=dict(color='#b4c7db', width=5)))
                fig.add_trace(go.Scatter(x=age_dist_train.index.astype(str), y=age_dist_train, mode='lines+markers', name='8기(19,20,21)', line=dict(color='#ed7777', width=5)))
                fig.update_layout(title="만나이에 따른 고혈압 비율 (train vs test)", xaxis_title="만나이", yaxis_title="고혈압 비율", yaxis_autorange=True, plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)

        elif pick_column == "체중":
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=weight_dist_test.index.astype(str), y=weight_dist_test, mode='lines+markers', name='9기(22)', line=dict(color='#b4c7db', width=5)))
                fig.add_trace(go.Scatter(x=weight_dist_train.index.astype(str), y=weight_dist_train, mode='lines+markers', name='8기(19,20,21)', line=dict(color='#ed7777', width=5)))
                fig.update_layout(title="체중에 따른 고혈압 비율 (train vs test)", xaxis_title="체중", yaxis_title="고혈압 비율",  plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)',yaxis_autorange=True)
                st.plotly_chart(fig)

            # WHtR에 따른 고혈압 비율 비교 (train vs test)  
        elif pick_column == "WHtR":
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=whtr_dist_test.index.astype(str), y=whtr_dist_test, mode='lines+markers', name='9기(22)', line=dict(color='#b4c7db', width=5)))
                fig.add_trace(go.Scatter(x=whtr_dist_train.index.astype(str), y=whtr_dist_train, mode='lines+markers', name='8기(19,20,21)', line=dict(color='#ed7777', width=5)))
                fig.update_layout(title="WHtR에 따른 고혈압 비율 (train vs test)", xaxis_title="WHtR", yaxis_title="고혈압 비율", yaxis_autorange=True, plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)

            # 허리둘레에 따른 고혈압 비율 비교 (train vs test)
        elif pick_column == "허리둘레":
                fig = go.Figure()
                fig.add_trace(go.Scatter(x=waist_dist_test.index.astype(str), y=waist_dist_test, mode='lines+markers', name='9기(22)', line=dict(color='#b4c7db', width=5)))
                fig.add_trace(go.Scatter(x=waist_dist_train.index.astype(str), y=waist_dist_train, mode='lines+markers', name='8기(19,20,21)', line=dict(color='#ed7777', width=5)))
                fig.update_layout(title="허리둘레에 따른 고혈압 비율 (train vs test)", xaxis_title="허리둘레", yaxis_title="고혈압 비율", yaxis_autorange=True, plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)
    with b:
        # 성별, 당뇨병 여부, 이상지질혈증 여부 비율 계산 (train만)
        gender_dist_train = calculate_proportions(df_train.copy(), '성별')
        diabetes_dist_train = calculate_proportions(df_train.copy(), '당뇨병 유병여부(19세이상)')
        dyslipidemia_dist_train = calculate_proportions(df_train.copy(), '이상지질혈증 여부')

        # 성별, 당뇨병 여부, 이상지질혈증 여부 비율 계산 (test만)
        gender_dist_test = calculate_proportions(df_test.copy(), '성별')
        diabetes_dist_test = calculate_proportions(df_test.copy(), '당뇨병 유병여부(19세이상)')
        dyslipidemia_dist_test = calculate_proportions(df_test.copy(), '이상지질혈증 여부')
        pick_column2 = st.selectbox("칼럼별 고혈압 비율 Train vs Test 원형 그래프", 
                                    ["성별","당뇨병 유병여부","이상지질혈증 유병여부"])
        
        if pick_column2 == "성별":
            col1,col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[go.Pie(labels=['남성', '여성'], values=[gender_dist_train[1], gender_dist_train[2]], hole=.3, marker=dict(colors=['#1f77b4', '#ed7777']))])
                fig.update_layout(title="고혈압 비율 속 성별 퍼센트(8기)",  plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)
            with col2:
                fig = go.Figure(data=[go.Pie(labels=['남성', '여성'], values=[gender_dist_test[1], gender_dist_test[2]], hole=.3, marker=dict(colors=['#72b1df', '#e6adae']))])
                fig.update_layout(title="고혈압 비율 속 성별 퍼센트(9기)",  plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)
        
        if pick_column2 == "당뇨병 유병여부":
            col1,col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[go.Pie(labels=['당뇨병 없음', '당뇨병 있음'], values=[diabetes_dist_train[0], diabetes_dist_train[1]], hole=.3, marker=dict(colors=['#1f77b4', '#ed7777']))])
                fig.update_layout(title="고혈압 비율 속 당뇨병 유병 퍼센트(8기)",  plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)
            with col2:
                fig = go.Figure(data=[go.Pie(labels=['당뇨병 없음', '당뇨병 있음'], values=[diabetes_dist_test[0], diabetes_dist_test[1]], hole=.3, marker=dict(colors=['#72b1df', '#e6adae']))])
                fig.update_layout(title="고혈압 비율 속 당뇨병 유병 퍼센트(9기)",  plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)
        if pick_column2 == "이상지질혈증 유병여부":
            col1,col2 = st.columns(2)
            with col1:
                fig = go.Figure(data=[go.Pie(labels=["이상지질혈증 없음", "이상지질혈증 있음"], values=[dyslipidemia_dist_train[0], dyslipidemia_dist_train[1]], hole=.3, marker=dict(colors=['#1f77b4', '#ed7777']))])
                fig.update_layout(title="고혈압 비율 속 이상지질혈증 유병 퍼센트(8기)",plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)
            with col2:
                fig = go.Figure(data=[go.Pie(labels=["이상지질혈증 없음", "이상지질혈증 있음"], values=[dyslipidemia_dist_test[0], dyslipidemia_dist_test[1]], hole=.3 , marker=dict(colors=['#72b1df', '#e6adae']))])
                fig.update_layout(title="고혈압 비율 속 이상지질혈증 유병 퍼센트(9기)",  plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                st.plotly_chart(fig)
    

    # 전처리 로직
    # ---------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------

    # 전처리 데이터 불러오기
    dff = csv(what='train') # 전처리진행시 오류 발생 할 수도있으니 다시 불러오기
    dff = dff[dff['만나이']<80]
    before = csv(what='train') # 그래프 비교를 위해 하나 더 불러옴
    before = before[before['만나이']<80]
    # 시각화할 변수 칼럼 리스트
    show = ['만나이', '체중','성별', '이상지질혈증 여부', '당뇨병 유병여부(19세이상)', 'WHtR_category','음주 점수', '신체활동점수','Target']
    start = dff.copy()

    # 로그변환
    start['신체활동점수'] = np.log1p(start['신체활동점수'])
    # 로그변환 끝 
    # 로그변환 df = start
    # ---------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------
    for col in ['신장', '허리둘레', '체중']:
            step1 = remove_outliers(start, col)
            step1_1 = remove_outliers(start, col) # 결측값 처리 안한 데이터프레임 보여주기 위해 하나 더 할당
    threshold_body = step1['신체활동점수'].quantile(0.90)
    step1 = step1[step1['신체활동점수'] <= threshold_body]   
    threshold_body = step1_1['신체활동점수'].quantile(0.90)
    step1_1 = step1_1[step1_1['신체활동점수'] <= threshold_body]   

    threshold_al = step1['음주 점수'].quantile(0.99)
    step1 = step1[step1['음주 점수'] <= threshold_al]
    threshold_al = step1_1['음주 점수'].quantile(0.99)
    step1_1 = step1_1[step1_1['음주 점수'] <= threshold_al]
    # 이상치 처리 끝 
    # 이상치 처리 df = step1 , step1_1 
    # ---------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------
    # 결측값 처리
    numeric_features = ['만나이', '체중', '음주 점수', '신체활동점수']
    categorical_features = ['성별', '이상지질혈증 여부', '당뇨병 유병여부(19세이상)', 'WHtR_category']
    step1[numeric_features] = step1[numeric_features].fillna(step1[numeric_features].mean())
    step1[categorical_features] = step1[categorical_features].fillna(step1[categorical_features].mode().iloc[0])
    step2 = step1.copy()
    # 결측값 처리 끝 
    # 결측값 처리 df = step2
    # ---------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------
    # SMOTENC 적용

    # 범주형 변수와 수치형 변수 구분
    numeric_features = ['만나이', '체중', '음주 점수', '신체활동점수']
    categorical_features = ['성별', '이상지질혈증 여부', '당뇨병 유병여부(19세이상)', 'WHtR_category']

    X = step2[numeric_features + categorical_features]
    y = step2['Target']
    categorical_feature_indices = [X.columns.get_loc(col) for col in categorical_features]

    smote_nc = SMOTENC(categorical_features=categorical_feature_indices, random_state=42)
    X_resampled, y_resampled = smote_nc.fit_resample(X, y)
    step3 = pd.DataFrame(X_resampled, columns=numeric_features + categorical_features)
    step3['Target'] = y_resampled
    # SMOTENC 끝 (전처리 종료)
    # SMOTENC df = step3 (최종)

    # 전처리 페이지 표시 나눔
    # ---------------------------------------------------------------------------------------------------- ----------------------------------------------------------------------------------------------------
    st.markdown('<b style="color:#31333f; font-size: 40px;">*전처리 시각화 대시보드*</b>', unsafe_allow_html=True)
    # 전처리 단계 선택

    tab1,tab2,tab3,tab4,tab5 = st.tabs(["1.로그 변환", "2.이상치 제거", "3.결측값 처리", "4.오버샘플링", "5.최종 데이터"])

    with tab1:
        col1 , col2 = st.columns(2)
        with col1:
            st.write("### 로그 변환 후 데이터")
            st.write(start[show].sample(10))
        with col2:
            st.write('### 로그 변환 후 신체활동 점수 히스토그램')
            fig2 = px.histogram(start, x=start['신체활동점수'],nbins=40,color_discrete_sequence=['#ed7777'],opacity=0.75)

            fig2.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
            st.plotly_chart(fig2)
    with tab2:
        st.write(f'### 이상지 제거 후 총 데이터 : {len(step1)}명')
        
        # 데이터 길이 확인
        print("step1_1 길이:", len(step1_1))
        print("before['체중'] 길이:", len(before['체중']))

        # 데이터프레임 길이 맞추기
        step1_1 = step1_1.reset_index(drop=True)
        before = before.reset_index(drop=True)

        # 히스토그램 생성
        weight_before = px.histogram(
            before,  # step1_1 대신 before 데이터프레임 직접 사용
            x='체중', 
            title="이상치 제거 전 체중",
            color_discrete_sequence=['#e6adae'],
            opacity=0.75
        )
        weight_before.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        st.plotly_chart(weight_before)
        linesero()
        height_before = px.histogram(step1_1, x=step1_1['신장'], title=f"이상치 제거 전 신장",color_discrete_sequence=['#e6adae'],opacity=0.75)
        height_before.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        st.plotly_chart(height_before)
        linesero()
        hip_before = px.histogram(step1_1, x=step1_1['허리둘레'], title=f"이상치 제거전 허리둘레",color_discrete_sequence=['#e6adae'],opacity=0.75)
        hip_before.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
        st.plotly_chart(hip_before)                
        col1,col2,col3,col4,col5 = st.columns([3,0.5,3,0.5,3])
        with col1:
            weight_after = px.histogram(step1, x=step1['체중'], title=f"이상치 제거후 체중",color_discrete_sequence=['#ed7777'],opacity=0.75)
            weight_after.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
            st.plotly_chart(weight_after) 
        with col2:
            linesero()
        with col3:
            height_after = px.histogram(step1, x=step1['신장'], title=f"이상치 제거후 신장",color_discrete_sequence=['#ed7777'],opacity=0.75)
            height_after.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
            st.plotly_chart(height_after)
        with col4:
            linesero()
        with col5:
            hip_after = px.histogram(step1, x=step1['허리둘레'], title=f"이상치 제거후 허리둘레",color_discrete_sequence=['#ed7777'],opacity=0.75)
            hip_after.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
            st.plotly_chart(hip_after)

    with tab3:
        col1 , col2 = st.columns(2)
        with col1:
            st.write("### 결측값 처리 전 데이터")
            st.write(step1_1[show].tail(10))
        with col2:
            st.write("### 결측값 처리 후 데이터")
            st.write(step2[show].tail(10))

    with tab4:
        col1, col2 = st.columns(2)
        with col1:
            st.write(f'### 샘플링 후 총 데이터 : {len(step3)}명')
            st.write(step3.head(10))
        with col2:
            selected_x = st.selectbox('칼럼 선택', step3[show].columns, key="x_axis")
            smote_fig = px.histogram(step3, x=selected_x, title=f"샘플링 후 {selected_x} 히스토그램",nbins=30,color_discrete_sequence=['#ed7777'])
            smote_fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
            st.plotly_chart(smote_fig)

    with tab5:
        col1, col2 = st.columns(2)
        with col1:
            st.write("### 최종 Train 데이터")
            st.write(step3.head(10))
        with col2:
            # 선택할 기준(변수) 선택
            columns = step3.columns.tolist()
            x_axis = st.selectbox('X축 변수 선택', columns)
            y_axis = 'Target'  # y축은 Target으로 고정
            chart_type = '히스토그램'

            # 체크박스 생성
            show_target_0 = st.checkbox('고혈압 없음')
            show_target_1 = st.checkbox('고혈압 있음')

            # 필터링 로직
            filtered_df = pd.DataFrame()

            if show_target_0:
                filtered_df = step3[step3['Target'] == 0]

            if show_target_1:
                filtered_df = pd.concat([filtered_df, step3[step3['Target'] == 1]])

            # Plotly를 사용한 그래프 그리기 (데이터가 있을 때만 그리기)
            if not filtered_df.empty:
                if chart_type == '히스토그램':
                    fig = px.histogram(filtered_df, x=x_axis, color='Target', title=f'{x_axis} 히스토그램',nbins=30,color_discrete_map={0: '#1f77b4', 1: '#ed7777'})
                    fig.update_layout(plot_bgcolor='rgba(0, 0, 0, 0)', paper_bgcolor='rgba(0, 0, 0, 0)')
                    fig.for_each_trace(lambda t: t.update(name = '고혈압 없음' if t.name == '0' else '고혈압 있음'))
                    st.plotly_chart(fig)
            else:
                st.write("선택된 Target 값에 대한 데이터가 없습니다.")
