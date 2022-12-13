import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import streamlit as st
import filterdf
import plot_graph1

data_url = "BankChurners.csv"

df = pd.read_csv(data_url)

st.set_page_config(
    page_title="BankChurners Dashboard",
    page_icon="🦈",
    layout="wide",
    initial_sidebar_state="expanded",
)

st.markdown("<h1 style='text-align: center;'>BankChurners Dashboard</h1> <p>Utilize o menu lateral para filtrar o dataset.</p>", unsafe_allow_html=True)
showdatafrane = st.sidebar.checkbox("Mostrar Dataset")

if showdatafrane:
    st.sidebar.title("Filtrar Dataset")
    st.dataframe(filterdf.filter_dataset(df))
else:
    st.write("Para visualizar o Dataset, marque a caixa de seleção no menu lateral.")

chart_data = pd.DataFrame(
    np.random.randn(20, 3),
    columns=["Gender", "Customer_Age", "Credit_Limit"]
)

st.bar_chart(chart_data)

# plot graph 1
#categoria_grafico = st.sidebar.selectbox('Selecione a categoria para apresentar no gráfico', options = df['Gender'].unique())
figura = plot_graph1.plot_graph(df)
st.pyplot(figura)


