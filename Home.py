import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from PIL import Image
import numpy as np
from filter import filter_dataset

from services.survey import survey

# Streamlit page configs
st.set_page_config(
    page_title="BankChurners Dashboard",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded",
)
st.set_option('deprecation.showPyplotGlobalUse', False)

# Dataset source
dataset = pd.read_csv("./assets/BankChurners.csv")

# Page title
st.markdown("<h1 style='text-align: center;color: #c9c904'>Credit Card Customers</h1> ", unsafe_allow_html=True)
st.markdown("***")

# Sidebar
st.sidebar.title("Menu")
showdataset = st.sidebar.checkbox("Visualizar dataset")

if showdataset:
    st.sidebar.title("Filtrar Dataset")
    st.write("Utilize o menu lateral para filtrar o dataset.")
    st.dataframe(filter_dataset(dataset))

lowestcredit = dataset[dataset['Credit_Limit'] <= 2500]['Education_Level'].value_counts()
lowcredit = dataset[dataset['Credit_Limit'] <= 4000][dataset['Credit_Limit'] > 2500]['Education_Level'].value_counts()
mediumcredit = dataset[dataset['Credit_Limit'] <= 8000][dataset['Credit_Limit'] > 4000]['Education_Level'].value_counts()
highcredit = dataset[dataset['Credit_Limit'] <= 17000][dataset['Credit_Limit'] > 8000]['Education_Level'].value_counts()
highestcredit = dataset[dataset['Credit_Limit'] > 17000]['Education_Level'].value_counts()



# options = dataset

category_names = ['Uneducated','High School', 'College', 'Graduate',  'Post-Graduate', 'Doctorate']
results = {
    'Até 2.500 de crédito': [lowestcredit.filter(regex='Uneducated', axis=0)[0], lowestcredit.filter(regex='High School', axis=0)[0], lowestcredit.filter(regex='College', axis=0)[0], lowestcredit.filter(regex='Graduate', axis=0)[0],  lowestcredit.filter(regex='Post-Graduate', axis=0)[0],  lowestcredit.filter(regex='Doctorate', axis=0)[0]],
    'Entre 2.500 e 4000': [lowcredit.filter(regex='Uneducated', axis=0)[0], lowcredit.filter(regex='High School', axis=0)[0], lowcredit.filter(regex='College', axis=0)[0], lowcredit.filter(regex='Graduate', axis=0)[0],  lowcredit.filter(regex='Post-Graduate', axis=0)[0],  lowcredit.filter(regex='Doctorate', axis=0)[0]],
    'Entre 4.000 e 8000': [mediumcredit.filter(regex='Uneducated', axis=0)[0], mediumcredit.filter(regex='High School', axis=0)[0], mediumcredit.filter(regex='College', axis=0)[0], mediumcredit.filter(regex='Graduate', axis=0)[0],  mediumcredit.filter(regex='Post-Graduate', axis=0)[0],  mediumcredit.filter(regex='Doctorate', axis=0)[0]],
    'Entre 8.000 e 17000': [highcredit.filter(regex='Uneducated', axis=0)[0], highcredit.filter(regex='High School', axis=0)[0], highcredit.filter(regex='College', axis=0)[0], highcredit.filter(regex='Graduate', axis=0)[0],  highcredit.filter(regex='Post-Graduate', axis=0)[0],  highcredit.filter(regex='Doctorate', axis=0)[0]],
    'Superior a 17000': [highestcredit.filter(regex='Uneducated', axis=0)[0], highestcredit.filter(regex='High School', axis=0)[0], highestcredit.filter(regex='College', axis=0)[0], highestcredit.filter(regex='Graduate', axis=0)[0],  highestcredit.filter(regex='Post-Graduate', axis=0)[0],  highestcredit.filter(regex='Doctorate', axis=0)[0]],
}



# Enable graphics
st.sidebar.title("Gráficos")
enable_graphics = st.sidebar.checkbox("Habilitar gráficos")

if enable_graphics:

    graph = st.sidebar.radio(" ", options=('Limite de crédito por categoria de renda', 'Faixa de limite de crédito por nível de escolaridade', 'Categoria de cartão de crédito por gênero' , 'Limite de crédito por coluna a ser selecionada', 'Clientes perdidos por coluna a ser selecionada' ))

    if graph == 'Limite de crédito por categoria de renda':

        credit_limit = dataset["Credit_Limit"].groupby(dataset["Income_Category"]).mean()

        st.markdown("<h3 style='text-align: center;color: #d87093'>Limite de crédito por categoria de renda</h3> ", unsafe_allow_html=True)
        feg = plt.figure(figsize=(15,7))
        sns.barplot(data=dataset, x=credit_limit.index, y=credit_limit.values,
        palette="Set2", dodge=False, order=['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +'])
        plt.ylabel("Limite de crédito médio")
        plt.xlabel("Categoria de renda")
        st.pyplot(feg)
        
        st.write(credit_limit)
        
    elif graph == 'Faixa de limite de crédito por nível de escolaridade':

        st.markdown("<h3 style='text-align: center;color: #d87093'>Faixa de limite de crédito por nível de escolaridade</h3> ", unsafe_allow_html=True)
        figure, axw = survey(results, category_names)
        st.pyplot(figure)

    elif graph == 'Categoria de cartão de crédito por gênero':

        st.markdown("<h3 style='text-align: center;color: #d87093'>Categoria de cartão de crédito por gênero</h3>", unsafe_allow_html=True)

        male = dataset["Card_Category"].where(dataset["Gender"] == "M").value_counts().values
        female =  dataset["Card_Category"].where(dataset["Gender"] == "F").value_counts().values
        card_categorys = (dataset["Card_Category"].value_counts()).index

        f = plt.figure()
        f.set_figwidth(4)
        f.set_figheight(2)
        plt.bar(card_categorys, female, color="#6495ED")
        plt.bar(card_categorys, male, bottom=female, color="#6A5ACD")
        plt.legend(["F", "M"])
        fig = plt.plot()
        st.pyplot(fig)

        st.markdown("<h4 style='text-align: center;color: #dab99c'>Escala maior</h3> ", unsafe_allow_html=True)
        plt.bar(card_categorys, female, color="#6495ED")
        plt.bar(card_categorys, male, bottom=female, color="#6A5ACD")
        plt.legend(["F", "M"])
        plt.ylim(0, 600)
        fig = plt.plot()
        st.pyplot(fig)

        st.write("Clientes homens por categoria de cartão de crédito:")
        st.write(dataset["Card_Category"].where(dataset["Gender"] == "M").value_counts())
        st.write("Clientes mulheres por categoria de cartão de crédito:")
        st.write(dataset["Card_Category"].where(dataset["Gender"] == "F").value_counts())

    elif graph == 'Limite de crédito por coluna a ser selecionada':

        eixoX = st.sidebar.selectbox("Selecione a coluna desejada:", dataset.columns.delete(0))
        
        credit_limit = dataset["Credit_Limit"].groupby(dataset[f"{eixoX}"]).mean()

        st.markdown(f"<h3 style='text-align: center;color: #d87093'>Gráfico interativo: Limite de crédito X {eixoX}</h3> ", unsafe_allow_html=True)
        feg = plt.figure(figsize=(15,7))
        sns.barplot(data=dataset, x=credit_limit.index, y=credit_limit.values,
        palette="Set2", dodge=False)
        plt.ylabel("Limite de crédito médio")
        plt.xlabel(f"{eixoX}")
        st.pyplot(feg)
    
    elif graph == 'Clientes perdidos por coluna a ser selecionada':

        eixoX = st.sidebar.selectbox("Selecione a coluna desejada:", dataset.columns.delete([0, 1]))

        st.markdown(f"<h3 style='text-align: center;color: #d87093'>Gráfico interativo: Clientes perdidos por {eixoX}</h3> ", unsafe_allow_html=True)
        
        attrited_customers = dataset["Attrition_Flag"].where(dataset["Attrition_Flag"] == 'Attrited Customer')

        data_eixoX = (dataset[f'{eixoX}'].value_counts()).index.tolist()
        data = []

        for d in data_eixoX:
            test = attrited_customers.where(dataset[f'{eixoX}'] == d).value_counts().values
            if test:
                data.append(attrited_customers.where(dataset[f'{eixoX}'] == d).value_counts().values[0])
            else:
                data.append(0)
        
        data = pd.Series(data)

        feg = plt.figure(figsize=(15,7))
        sns.barplot(data=dataset, x=data_eixoX, y=data.values,
        palette="Set2", dodge=False)
        plt.ylabel("Clientes perdidos")
        plt.xlabel(f"{eixoX}")
        st.pyplot(feg)

    else:
        st.write('Erro. Recarregue a página e tente novamente.')
        
if not enable_graphics and not showdataset:

    image = Image.open('./assets/Credit card-bro.png')

    col1, col2, col3 = st.columns([1,2,1])

    with col1:
        st.write("")

    with col2:
        st.image(image, width=350)

    with col3:
        st.write("")

    st.write("Este dataset consiste em dados de 10.000 usuários de cartão de crédito de um determinado", 
    "banco. Esses dados consistem em idade, salário, estado civil, nível de escolaridade, gênero, ",
    "entre outras informações relevantes.")

    st.write("O dataset foi obtido através do seguinte link: (https://www.kaggle.com/datasets/sakshigoyal7/credit-card-customers)")