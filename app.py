import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
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
st.markdown("<h1 style='text-align: center;color: yellow'>BankChurners Dashboard</h1> <p>Utilize o menu lateral para filtrar o dataset.</p>", unsafe_allow_html=True)

showdataset = st.sidebar.checkbox("Ver dataset")

if showdataset:
    st.sidebar.title("Filtrar Dataset")
    st.dataframe(filter_dataset(dataset))
else:
    st.write("Para visualizar o Dataset, marque a caixa de seleção no menu lateral.")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Gender", "Customer_Age", "Credit_Limit"]
)

#st.bar_chart(chart_data)

# plot graph 1
#categoria_grafico = st.sidebar.selectbox('Selecione a categoria para apresentar no gráfico', options = dataset['Gender'].unique())
#figura = plot_graph1.plot_graph(dataset)
#st.pyplot(figura)


