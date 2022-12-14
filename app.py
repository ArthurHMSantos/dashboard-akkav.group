import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np
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

st.sidebar.title("Menu")
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


# credit_limit = 

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


def survey(results, category_names):
    """
    Parameters
    ----------
    results : dict
        A mapping from question labels to a list of answers per category.
        It is assumed all lists contain the same number of entries and that
        it matches the length of *category_names*.
    category_names : list of str
        The category labels.
    """
    labels = list(results.keys())
    data = np.array(list(results.values()))
    data_cum = data.cumsum(axis=1)
    category_colors = plt.colormaps['RdYlGn'](
        np.linspace(0.15, 0.85, data.shape[1]))

    fig, ax = plt.subplots(figsize=(13, 5))
    ax.invert_yaxis()
    ax.xaxis.set_visible(False)
    ax.set_xlim(0, np.sum(data, axis=1).max())

    for i, (colname, color) in enumerate(zip(category_names, category_colors)):
        widths = data[:, i]
        starts = data_cum[:, i] - widths
        rects = ax.barh(labels, widths, left=starts, height=0.5,
                        label=colname, color=color)

        r, g, b, _ = color
        text_color = 'white' if r * g * b < 0.5 else 'darkgrey'
        ax.bar_label(rects, label_type='center', color=text_color)
    ax.legend(ncol=len(category_names), bbox_to_anchor=(0, 1),
              loc='lower left', fontsize='small')

    return fig, ax




#plot graph 1 ----------------
st.sidebar.title("Habilitar Gráficos")
gfc_1 = st.sidebar.checkbox("Gráfico 1")
gfc_2 = st.sidebar.checkbox("Gráfico 2")
gfc_3 =st.sidebar.checkbox("Gráfico 3")

if gfc_1:
    feg = plt.figure(figsize=(15,7))
    sns.barplot(data=dataset, x=income_count.values, y=credit_limit.index, hue=income_count.values, 
    palette="Set2", dodge=False, order=['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +'])
    plt.xlabel("Limite de crédito médio")
    plt.ylabel("Categoria de renda")
    st.markdown("<h3 style='text-align: center;color: black'>Limite de crédito médio por categoria de renda</h3> ", unsafe_allow_html=True)
    st.pyplot(feg)
if gfc_2:

    figure, axw = survey(results, category_names)
    st.markdown("<h3 style='text-align: center;color: black'>Faixa de limite de crédito por nível de escolaridade</h3> ", unsafe_allow_html=True)
    st.pyplot(figure)

if gfc_3:
    eixoX = st.sidebar.selectbox("Selecione o eixo X para mudar o grafíco 3", dataset.columns)
    eixoY = 'Credit_Limit'
    #st.line_chart(data=dataset, x = eixoX, y= eixoY, width=0, height=0, use_container_width=True)
    st.bar_chart(data=dataset, x = eixoX, y= eixoY, width=0, height=0, use_container_width=True)
    #st.area_chart(data=dataset, x = eixoX, y= eixoY, width=0, height=0, use_container_width=True)


