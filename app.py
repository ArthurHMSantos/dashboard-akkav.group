import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from filter import filter_dataset, filter_graphs
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

show_graph_filters = st.sidebar.checkbox("Habilitar filtros para gráficos")

# options = dataset

if show_graph_filters:
    dataset = filter_graphs(dataset)


income_count = dataset['Income_Category'].value_counts()
credit_limit = dataset["Credit_Limit"].groupby(dataset["Income_Category"]).mean()

fg = plt.figure(figsize=(15,7))
sns.barplot(data=dataset, x=income_count.index , y=income_count.values, hue=income_count.index, palette="Set2", dodge=False)
st.pyplot(fg)

feg = plt.figure(figsize=(15,7))
sns.barplot(data=dataset, x=income_count.values, y=credit_limit.index, hue=income_count.values, 
    palette="Set2", dodge=False, order=['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +'])
plt.xlabel("Limite de crédito médio")
plt.ylabel("Categoria de renda")
st.pyplot(feg)
