import streamlit as st
from assets.banchurners import predicting_churn

st.set_page_config(page_title="Simulação", page_icon="💸")

st.markdown("<h1 style='color: #c9c904; text-align: center;'>Simulação</h1>", unsafe_allow_html=True)

with st.form(key='my_form'):
    col1, col2 = st.columns(2)
    with col1:
        st.write("Dados Pessoais")
        gender = st.radio("Gênero", ["Feminino", "Masculino"])
        age = st.number_input("Idade", min_value=18, max_value=100, value=25)
        education_level = st.selectbox("Nível de Escolaridade", ["Sem Educação", "Ensino Médio", "Ensino Superior", "Mestrado", "Pós-graduação/Especialização", "Doutorado", "Não informado"])
        marital_status = st.selectbox("Estado Civil", ["Casado(a)", "Solteiro(a)", "Divorciado(a)", "Não informado"])
        months_on_book = st.number_input("Meses de relacionamento com o banco", min_value=0, value=12)
    with col2:
        st.write("Dados Financeiros")
        income_category = st.selectbox("Faixa de Renda", ["Menos de $40K", "$40K - $60K", "$60K - $80K", "$80K - $120K", "$120K +", "Não informado"])
        card_category = st.selectbox("Categoria do Cartão", ["Blue", "Silver", "Gold", "Platinum"])
        dependent_count = st.number_input("Número de Dependentes", min_value=0, value=0)
        credit_limit = st.number_input("Limite de Crédito", value=5000, step=100)
        avg_open_to_buy = st.number_input("Valor médio disponível para compras", value=1000, step=100)
        avg_utilization_ratio = st.slider("Taxa média de utilização de crédito", min_value=0.0, max_value=1.0, step=0.05)
    submit_button = st.form_submit_button(label='Simular')
    
if submit_button:
    gender_dict =  {"Feminino": "F", "Masculino": "M"}
    education_level_dict = {
        "Sem Educação": "Uneducated",
        "Ensino Médio": "High School",
        "Ensino Superior": "College",
        "Mestrado": "Graduate",
        "Pós-graduação/Especialização": "Post-Graduate",
        "Doutorado": "Doctorate",
        "Não informado": "Unknown"
    }
    marital_status_dict = {
        "Casado(a)": "Married",
        "Solteiro(a)": "Single",
        "Divorciado(a)": "Divorced",
        "Não informado": "Unknown"
    }
    income_category_dict = {
        "Menos de $40K": "Less than $40K",
        "$40K - $60K": "$40K - $60K",
        "$60K - $80K": "$60K - $80K",
        "$80K - $120K": "$80K - $120K",
        "$120K +": "$120K +",
        "Não informado": "Unknown"
    }
    gender_input = gender_dict[gender]
    education_level = education_level_dict[education_level]
    marital_status = marital_status_dict[marital_status]
    income_category = income_category_dict[income_category]
    user_input = [age, gender_input, dependent_count, education_level, marital_status, income_category, card_category, credit_limit, months_on_book, avg_open_to_buy, avg_utilization_ratio]
    result = predicting_churn(user_input)
    st.write(f"Resultado da Simulação: **{result}**")