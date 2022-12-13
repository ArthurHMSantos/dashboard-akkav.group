import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from filters import filter_dataset
import plot_graph1

# Dataset source
dataset = pd.read_csv("BankChurners.csv")

# Streamlit page configs
st.set_page_config(
    page_title="BankChurners Dashboard",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Page title
st.markdown("<h1 style='text-align: center;color: black'>BankChurners Dashboard</h1> ", unsafe_allow_html=True)

showdataset = st.sidebar.checkbox("Ver dataset")

if showdataset:
    st.sidebar.title("Filtrar Dataset")
    st.write("Utilize o menu lateral para filtrar o dataset.")
    st.dataframe(filter_dataset(dataset))

else:
    st.write("Para visualizar o Dataset, marque a caixa de seleção no menu lateral.")

#plot graph 1 ----------------
st.sidebar.title("Fitros para gráficos")
# options = dataset
gen_options = dataset["Gender"].unique()
gen = st.selectbox("Selecione o genero do cliente", gen_options)
dataset = dataset[dataset["Gender"] == gen]

age_options = dataset["Customer_Age"].unique()
age = st.selectbox("Selecione a idade do cliente: ", age_options)
dataset = dataset[dataset["Customer_Age"] == age]

edu_options = dataset["Education_Level"].unique()
edu = st.selectbox("Selecione o Nível de Educação", edu_options)
dataset = dataset[dataset["Education_Level"] == edu]

card_options = dataset["Card_Category"].unique()
card_type = st.selectbox('Selecione o tipo de cartão:', card_options)
dataset = dataset[dataset["Card_Category"] == card_type]

income_count = dataset['Income_Category'].value_counts()

fg = plt.figure(figsize=(15,7))
sns.barplot(data=dataset, x=income_count.index , y=income_count.values, hue=income_count.index, palette="Set2", dodge=False)
st.pyplot(fg)
