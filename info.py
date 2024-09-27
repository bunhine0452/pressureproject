import pandas as pd
import streamlit as st
from PIL import Image
from funcs import load_css, load_local_font, linegaro
import requests

def info_page():

    st.sidebar.markdown(
    """
    <div style="border-top: 3px solid #3F5277; width: 100%;"></div>
    """,
    unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 15px; color:rgba(246,244,241,1);"> 🤙 You can contact us with</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 13px; color:rgba(253,250,241,1);"> 김현빈</br>hb000122@gmail.com </p>', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 13px; color:rgba(253,250,241,1);"> 이정화</br>happychristmas1995@gmail.com</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 13px; color:rgba(253,250,241,1);"> 신상길</br>tkdrlfdk920@gmail.com</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 13px; color:rgba(253,250,241,1);"> 정다운</br>jdu1941@gmail.com</p>', unsafe_allow_html=True)
    st.sidebar.markdown("")
    st.sidebar.markdown(
        """
        <div align="center">
            <p style="font-size: 17px; color:rgba(246,244,241,1); margin-bottom: 0px;">Total views</p>
            <a href="https://www.cutercounter.com/" target="_blank">
                <img src="https://www.cutercounter.com/hits.php?id=huxqdpfk&nd=6&style=13" border="0" alt="hit counter">
            </a>
        </div>
        """, 
        unsafe_allow_html=True)

    logo = Image.open('./data/image/Teamicon-removebg-preview.png')
    a,b,c= st.columns([1,7,2])
    with a:
        st.image('./data/image/temp_logo2-removebg-preview.png')
    with b:
        st.title('PROJECT : 고혈압 예측모델')
    with c:
        # GitHub API를 사용하여 리포지토리 정보 가져오기
        repo_owner = "bunhine0452"
        repo_name = "pressureproject"

        # GitHub API 요청
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        response = requests.get(url)
        repo_info = response.json()

        # 필요한 정보 추출
        stars = repo_info.get("stargazers_count", 0)
        forks = repo_info.get("forks_count", 0)
        issues = repo_info.get("open_issues_count", 0)

        # GitHub 정보 표시
        st.markdown(f"[GitHub Repository](https://github.com/{repo_owner}/{repo_name})")
        st.markdown(f"⭐ Stars: {stars}")
        st.markdown(f"🍴 Forks: {forks}")
        st.markdown(f"🐞 Open Issues: {issues}")
    
    linegaro() 
    if 'count' not in st.session_state:
        st.session_state.count = 0
    
    def increment():
        st.session_state.count += 1

    # 첫 번째 화면은 항상 표시되도록 설정
    a, b = st.columns([2, 7])
    with a:
        st.image(logo, width=400)

    with b:
        st.markdown('####')
        team_title = '<b style="color:#31333f; font-size: 30px;">Team 고혈압</b>'
        st.markdown(team_title, unsafe_allow_html=True)
        st.write(
            """
            국민 건강 영양조사 원시데이터 자료를 분석하여 신체 데이터 및 설문 기반으로 여러 유사점을 찾고 분석한 이후 
            선별된 요인들을 토대로 고혈압을 예측할 수 있는 모델을 만들고 설문 조사를 받은 뒤 고혈압 확률뿐만 아니라 
            다양한 건강 대시보드를 통해 현재 자신의 신체 정보를 확인하며 여러 성인병을 예방할수 있는 방법을 챗봇을 이용하여 제시하는 것이 
            이번 프로젝트의 궁극적인 주제와 목적입니다.         
            """
        )
        st.write(
            """
            건강한 신체를 유지하며 성인병의 주된 원인이라고 자주 지목되는 고혈압을 
            “먼저 예방하는 것이 다양한 합병증을 예방할 수 있겠다” 라는 가설을 세우며 고혈압을 예방할 수 있는 모델을 만들게 되었습니다. 
            또한 자신의 생활 습관에 관한 설문과 자신이 알고 있는 신체 데이터를 통해서 고혈압 확률을 예측할 수 있도록 
            만들었고, 챗봇이 설문 결과에 따라서 알맞은 레시피를 추천할 수 있도록 노력하였습니다.      
            """
        )
        st.markdown('#####')
    # st.session_state.count == 0일 때만 버튼 표시
    if st.session_state.count == 0:
        st.button("다음 ⬇️", key='first', on_click=increment)

    # st.session_state.count가 1 이상일 때 추가 내용을 표시하고 버튼은 사라짐
    if st.session_state.count >= 1:
        #linegaro()
        st.markdown('#####')
        a, b = st.columns([2, 7])
        with a:
            st.image('./data/image/image2.png', width=350)           
        with b:
            st.markdown('####')
            st.markdown('<b style="color:#31333f; font-size: 30px;">고혈압이란?</b>', unsafe_allow_html=True)
            st.write(
                """
                    동맥을 지나는 혈액의 압력이 지속적으로 
                    정상 기준보다 높아진 상태를 말합니다.
                    우리나라 30세 이상의 인구 중 30%의 유병률을 보이며, 
                    세계적으로 사망 위험 요소 중 1위를 차지하는 만성질환으로,
                    심장 질환과 뇌졸중과 같은 심각한 건강 문제를 
                    초래할 수 있는 중요한 문제입니다.        
                """
            )
            st.write(
                """
                < 고혈압의 진단 기준 >
                """
            )
            st.markdown('<b style="font-size: 15px;">- 수축기 혈압: 140mmHg 이상</b>', unsafe_allow_html=True)
            st.markdown('<b style="font-size: 15px;">- 이완기 혈압: 90mmHg 이상</b>', unsafe_allow_html=True)
            st.write(
                '''
                    합병증이 나타나기 전까지 증상이 나타나지 않으며, 
                    환자 대부분이 원인을 알 수 없습니다.
                    이를 위해 고혈압은 미리 예방하는 것이 가장 중요합니다.   
                '''
            )
            st.markdown('#####')
    if st.session_state.count == 1:    
        st.button("다음 ⬇️", key='second', on_click=increment)

    if st.session_state.count >= 2:
        #linegaro()
        st.markdown('#####')
        a, b, c = st.columns([3, 3, 3])
        with a:
            st.image('./data/image/chat1.png', width=550)           
        with b:
            st.write("""
            ### 그래프 설명
            """,)
            st.write("""
                혈압 진료 현황에 따르면, 국내 고혈압 환자는 746만 명으로 
                전체 인구의 14.55%에 달하는 것으로 나타났습니다. 
                최근 5년간(2019~2023년) 고혈압 진료 추이를 분석한 결과
                환자 수가 14.1%(연평균 3.4%) 증가했으며, 남성의 증가율이 여성보다 높았습니다. 
                남성 환자는 5년간 16.3%(연평균 3.8%) 증가
                여성 환자는 11.9%(연평균 2.9%) 증가했습니다.
            """,)
            # 프로젝트 배경 및 목표
        with c:
            st.markdown("""
                ### 프로젝트 배경 및 목표
            """)
            st.markdown("""
                    고혈압은 심혈관 질환의 주요 원인 중 하나로, 만성적인 건강 문제를 유발할 수 있습니다.
                    해마다 고혈압 환자가 증가하는 추세이며 가장 위험한 만성질환 중 하나로 예상됩니다.
                    조기 발견과 관리가 중요하지만, 대부분의 경우 합병증이 나타날 때까지 증상이 미비하여 방치되는 경우가 많고
                    본 프로젝트는 국민건강영양조사 2019~2021 데이터셋을 기반으로 
                    고혈압 발생 가능성을 예측할 수 있는 모델을 개발하여
                    개인의 건강 리스크를 조기에 감지하고 적절한 예방 조치를 제공할 수 있는 솔루션을 목표로 합니다.
            """)
    if st.session_state.count == 2:    
        st.button("다음 ⬇️", key='third', on_click=increment)

    if st.session_state.count >= 3:
        #linegaro()
        st.markdown('#####')
        st.title('팀원소개')
        a, b, c, d = st.columns([2, 2, 2, 2])
        with a:
           st.markdown('### 김현빈')
           st.markdown('##### 모델 설계 및 챗봇 구현 및 streamlit 대시보드 구성')
           st.write(''' 
                    모델에 필요한 데이터를 다시 분석하기도 하고 다양한 모델 그리고 기법들을 활용하여 
                    지속적인 모니터링을 통해 서비스에 사용될 최종 모델을 만들었습니다. 
                    또한 이를 근거로 제시할 수 있는 여러 데이터셋을 시각화 하였습니다.
                    추가로 설문을 받아서 본인이 동나이 및 성별 대 위치를 제시하여 고혈압에 얼마나 노출되어있는지 알 수 있도록 구현하였습니다. 
                    챗봇구현에 기여하였습니다.
                    ''')
        with b:
           st.markdown('### 신상길')
           st.markdown('##### 데이터 이해와 분석과 챗봇 데이터를 크롤링 및 검색')
           st.write(''' 
                    다양한 피처 엔지니어링 방법을 공부하였고, 국민 건강 영양조사 데이터와 저희 팀의 방향성에 맞는 
                    여러 머신러닝 모델을 돌려보았으며, 가설을 세워서 나름대로 모델 을 구현 해보기도했습니다.
                    그 뒤로는 데이터 전처리 이전 부분을 스트림릿으로 구현해보았습니다. 
                    지금은 정화님이 기틀을 잡은 코드를 기반으로 OpenAI API를 통해 챗봇을 구현하고 있습니다.
                    또한 챗봇에 필요한 요리, 레시피 데이터를 전처리하였습니다.  
                    ''')
        with c:
           st.markdown('### 이정화')
           st.markdown('##### 데이터 전처리와 및 모델링 챗봇 구현 및 Rag stramlit 구현 ')
           st.write('''
                    전처리 과정에서 컬럼 선택과 모델링에 적극적으로 참여하였습니다. 
                    프로젝트에서는 챗봇구현을 담당하였는데 먼저 주차별 식단 데이터를 정리하고 
                    텍스트 청크로 분리하여 분석에 용이하도록 만들었습니다. 
                    이를 기반으로 임베딩과 벡터 스토어를 활용한 검색 시스템을 구축하여 
                    사용자가 입력한 질의에 따라 맞춤형 식단을 추천하는 챗봇을 구현했습니다.
                    마지막으로 이를 보여줄수 있는 Rag streamlit 페이지를 만들었습니다.
                    ''')
        with d:
           st.markdown('### 정다운')
           st.markdown('##### 데이터 시각화와 논리적 통계 담당')
           st.write(''' 
                    다양한 시각화를 통해 고혈압과 관련된 요인들을 찾아내고, 고혈압과 관련된 논문들을 읽어보고 
                    여러 근거들을 통해 시각화의 기틀을 만들었습니다. 
                    Streamlit을 사용하여 우리나라 고혈압 발병에 대한 통계와 
                    프로젝트를 이해하는 데 있어 설명해주는 페이지를 만들었습니다. 
                    ''')

        a,b,c = st.columns(3)
        with b:
            st.markdown('#')
            st.markdown('#')   
            st.image('./data/image/logos.png')

            st.markdown(
                """
                <div style="display: flex; justify-content: center; align-items: center; margin-top: 20px;">
                    <a href="https://highbloodpressure.streamlit.app" target="_blank" style="text-decoration: none;">
                        <div style="display: inline-block; padding: 10px 20px; background-color: rgb(83, 100, 147); color: white; border-radius: 5px; text-align: center; font-weight: bold;">
                            챗봇 모델 보러가기
                        </div>
                    </a>
                </div>
                """,
                unsafe_allow_html=True)
        
