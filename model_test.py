import streamlit as st
# funcs.py
from funcs import load_css, load_local_font, linegaro, linesero, csv , calculate_proportions , remove_outliers, model_result, model_result_hyper ,test22

def model_test_page():
    
        
    st.sidebar.markdown(
        """
        <div style="border-top: 3px solid #3F5277; width: 100%;"></div>
        """,
        unsafe_allow_html=True)
    st.sidebar.markdown('<p style="font-size: 18px; color:rgba(246,244,241,1);"> 🦥 이 페이지에선 모델 테스트 결과를 보실 수 있습니다.</p>', unsafe_allow_html=True)
    st.sidebar.markdown("")
    a, b = st.columns([1,7])
    with a:
        st.image('./data/image/temp_logo2-removebg-preview.png')
    with b:
        st.title('모델 테스트 Dashboard')
    linegaro()
    st.markdown('<b style="color:#31333f; font-size: 40px;">*Model results compare*</b>', unsafe_allow_html=True)
    a, b ,c= st.columns([1,0.05,1])
    with a:
        graph1 = st.selectbox('비교할 모델을 선택해주세요',('Logistic Regression','SVM','Random Forest','LGBM','Xgboost'),index=0)
        if st.checkbox('1.하이퍼 파라미터 튜닝 실행'):
            if graph1 == 'Logistic Regression':
                model_result_hyper(model='Logistic Regression')
            elif graph1 == 'SVM':
                model_result_hyper(model='SVM')
            elif graph1 == 'Random Forest':
                model_result_hyper(model='Random Forest')
            elif graph1 == 'LGBM':
                model_result_hyper(model='LGBM')
            elif graph1 == 'Xgboost':
                model_result_hyper(model='xg')
                      
        else:     
            if graph1 == 'Logistic Regression':
                model_result(model='Logistic Regression')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='Logistic Regression')
            elif graph1 == 'SVM':
                model_result(model='SVM')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='SVM')
            elif graph1 == 'Random Forest':
                model_result(model='Random Forest')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='Random Forest')
            elif graph1 == 'LGBM':
                model_result(model='LGBM')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='LGBM')
            elif graph1 == 'Xgboost':
                model_result(model='xg')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='xg')
    with b:
        st.markdown(
        """
        <div style="border-right: 2px solid #D4BDAC; height: 600px;"></div>
        """,
        unsafe_allow_html=True)
    with c:
        graph2 = st.selectbox('비교할 모델을 선택해주세요', ('Logistic Regression', 'SVM', 'Random Forest', 'LGBM','Xgboost'), index=3)
        if st.checkbox('2.하이퍼 파라미터 튜닝 실행'):
            if graph2 == 'Logistic Regression':
                model_result_hyper(model='Logistic Regression')
            elif graph2 == 'SVM':
                model_result_hyper(model='SVM')
            elif graph2 == 'Random Forest':
                model_result_hyper(model='Random Forest')
            elif graph2 == 'LGBM':
                model_result_hyper(model='LGBM')
            elif graph2 == 'Xgboost':
                model_result_hyper(model='xg')            
        else:     
            if graph2 == 'Logistic Regression':
                model_result(model='Logistic Regression')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='Logistic Regression')
            elif graph2 == 'SVM':
                model_result(model='SVM')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='SVM')
            elif graph2 == 'Random Forest':
                model_result(model='Random Forest')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='Random Forest')
            elif graph2 == 'LGBM':
                model_result(model='LGBM')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='LGBM')
            elif graph2 == 'Xgboost':
                model_result(model='xg')
                st.markdown('### 9기 데이터에 검증 결과')
                test22(model='xg')
    linegaro()
    st.markdown('<b style="color:#31333f; font-size: 40px;">*Final Model*</b>', unsafe_allow_html=True)
    st.write(
    """
    최종적으로 사용할 모델을 택하는데 있어, 저희는 다양한 평가지표를 통해서 모델의 성능을 평가할수 있었습니다. 그러나 막연히 점수가 높은 모델을 사용하기엔
    여러 문제들의 발생할 위험 요소들을 인지하며 모델에 학습시킬 수 있는 추가 데이터에 대한 대비(업데이트와 유지보수) 와 
    실제 모델 사용 기반으로 여럿 모니터링을 거치며 최종적으로 사용할 모델을 선택하였습니다. 
    """)
    st.markdown('<b style="color:#31333f; font-size: 20px;">Model to use:Logistic Regression</b>', unsafe_allow_html=True)
    # a, b = st.columns([7,3])
    # with a:
    st.markdown('<b style="color:#31333f; font-size: 20px;">Logistic Regression 의 Shap 그래프 </b>', unsafe_allow_html=True)
    st.image('./data/results/logi/logishap.png')
    # with b:
    #     st.markdown('<b style="color:#31333f; font-size: 20px;">LGBM의 의 Shap 그래프 </b>', unsafe_allow_html=True)
    #     st.image('./data/results/lgbm/lgbmshap2.png')
    #     st.markdown('<b style="color:#31333f; font-size: 20px;">Xgboost 의 Shap 그래프 </b>', unsafe_allow_html=True)
    #     st.image('./data/results/xg/xgshap.png')


    st.markdown('<b style="color:#31333f; font-size: 30px;">Information</b>', unsafe_allow_html=True)
    st.write(
        """
        프로젝트의 주요 목표는 사용자가 알고 있는 최대한의 건강 상태와 설문 데이터를 통해 고혈압 발생 확률을 예측하는 것입니다.
        모델을 학습시킬 때, 연속형 데이터와 범주형 데이터에 대해 처리된 정보가 손실되지 않고 적절하게 학습되었으며, 
        예측에 사용되는 모든 칼럼에 대한 고혈압 확률에 미치는 영향력이 적절하게 반영되었습니다. 
        예를 들어, 신체활동 점수가 낮을수록 고혈압 확률이 증가하며, 음주 점수, 체중 등 다른 칼럼들도 값이 높아질수록 고혈압 확률이 상승합니다.
        또한, '이상지질혈증 여부'와 '당뇨병 유병 여부'에 대한 의존성이 너무 높지 않을까 하는 우려가 있었지만, SHAP 그래프에서 성별을 제외한 나머지 칼럼들과 유사한 영향력을 보였습니다.

        모델의 단점으로는 만나이 칼럼에 대한 의존성이 높다는 점이 있습니다. 이로 인해 다음과 같은 문제가 발생할 수 있습니다:
        1. 연령이 높지만 건강한 사람도 고혈압으로 간주할 수 있음.
        2. 연령이 낮지만 건강하지 않은 사람을 고혈압으로 판단하지 않을 수 있음.

        이 문제를 해결하기 위해 저희 팀은 추후 모델의 실사용 시 여러 지표를 추가하여 사용자에게 단순히 고혈압 확률을 제공하는 것에 그치지 않고, 
        사용자의 만나이를 기준으로 ±5세 내에 해당하는 데이터 속에서 사용자의 위치를 상위 몇 퍼센트에 해당하는지도 제공할 예정입니다. 
        이를 통해 더욱 정확한 진단이 가능해집니다. 예를 들어, 고혈압 확률이 70% 이상이더라도 해당 군 내에서 상위 퍼센트가 높지 않다면 비교적 안심할 수 있으며, 
        반대로 고혈압 확률이 20%이지만 해당 군 내에서 상위 퍼센트가 높다면 고혈압에 대해 주의가 필요합니다.
        
        이렇게 저희는 단순히 정확도가 높고, 여러 지표들의 값이 잘 나오는 모델을 아닌, 데이터 왜곡과, 추가 데이터 학습 여부에 대한 가능성도 인지하며 유지보수가 가능한
        모델을 선택하였습니다.
        """)
