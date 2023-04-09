import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import numpy as np

from PIL import Image
from filter import filter_dataset
from survey import survey

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
dataset = dataset.iloc[:, :-2]

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

    graph = st.sidebar.radio(" ", options=('Limite de crédito por categoria de renda', 'Faixa de limite de crédito por nível de escolaridade', 'Categoria de cartão de crédito por gênero' , 'Limite de crédito por coluna a ser selecionada', 'Clientes perdidos por coluna a ser selecionada', 'Gráfico de Caixa por coluna a ser selecionada'))

    if graph == 'Limite de crédito por categoria de renda':

        credit_limit = dataset["Credit_Limit"].groupby(dataset["Income_Category"]).mean()

        st.markdown("<h2 style='text-align: center;color: #d87093'>Limite de Crédito por Categoria de Renda</h2>", unsafe_allow_html=True)

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.barplot(data=dataset, x=credit_limit.index, y=credit_limit.values,
                    palette="Set2", dodge=False, order=['Less than $40K', '$40K - $60K', '$60K - $80K', '$80K - $120K', '$120K +'])
        ax.set_ylabel("Limite de crédito médio")
        ax.set_xlabel("Categoria de renda")
        ax.set_title("Limite de Crédito Médio por Categoria de Renda")
        ax.grid(axis='y', linestyle='--')

        st.write("Esse gráfico permite a visualização do limite de crédito médio por categoria de renda.")

        st.pyplot(fig)

        st.write("É possível observar que a categoria de renda com maior limite de crédito é a de $$120K +, e a categoria de renda com menor limite de crédito é a de Less than $40K. Isso reforça a ideia de que quanto maior a renda, maior o limite de crédito nesse banco.")

        st.write(credit_limit)

        
    elif graph == 'Faixa de limite de crédito por nível de escolaridade':

        st.markdown("<h3 style='text-align: center;color: #d87093'>Faixa de limite de crédito por nível de escolaridade</h3> ", unsafe_allow_html=True)
        st.write("Esse gráfico permite a visualização do limite de crédito médio por nível de escolaridade.")
        figure, axw = survey(results, category_names)
        st.pyplot(figure)
        st.write("Com esse gráfico, pode-se identificar se existe uma correlação entre essas variáveis e se a instituição financeira tem políticas específicas para determinados grupos. É possível observar se há diferenças significativas entre os valores e se elas seguem um padrão, como, por exemplo, se o limite de crédito aumenta à medida que o nível de escolaridade aumenta. Essa análise pode fornecer insights valiosos para a instituição financeira em termos de ajustes nas políticas de crédito e adequação do público-alvo.")
        st.write("No entanto, é interessante observar que o nível de educação e o de renda não são variáveis independentes, pois, em geral, quanto maior o nível de educação, maior a renda. Portanto, é possível que a diferença entre os valores de limite de crédito seja explicada, em parte, pela diferença de renda entre os grupos.")

    elif graph == 'Categoria de cartão de crédito por gênero':

        st.markdown("<h3 style='text-align: center;color: #d87093'>Categoria de cartão de crédito por gênero</h3>", unsafe_allow_html=True)
        st.write("Esses gráficos permitem a visualização da categoria de cartão de crédito por gênero.")
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

        st.write("Com base na análise dos gráficos relacionados à categoria do cartão de crédito por gênero, podemos observar que a distribuição das categorias de cartão de crédito entre homens e mulheres está relativamente equilibrada, com proporções similares em todas as categorias. No entanto, é importante destacar que a categoria do cartão de crédito está diretamente relacionada ao limite de crédito e, por consequência, à renda do titular do cartão. Ao analisarmos o gráfico que compara o limite de crédito por categoria de renda, é possível notar que a maioria das mulheres no dataset não possui renda anual superior a 60 mil dólares, o que pode explicar a similaridade nas categorias de cartão de crédito entre homens e mulheres. Este fato ressalta a importância de considerar variáveis socioeconômicas ao analisar dados relacionados a cartões de crédito e seus titulares.")

        st.write("Clientes homens por categoria de cartão de crédito:")
        st.write(dataset["Card_Category"].where(dataset["Gender"] == "M").value_counts())
        st.write("Clientes mulheres por categoria de cartão de crédito:")
        st.write(dataset["Card_Category"].where(dataset["Gender"] == "F").value_counts())

    elif graph == 'Limite de crédito por coluna a ser selecionada':
        dataset = dataset.drop(['CLIENTNUM','Total_Relationship_Count', 'Total_Revolving_Bal', 'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio'], axis=1)
        eixoX = st.sidebar.selectbox("Selecione a coluna desejada:", dataset.columns.delete(0))
        
        credit_limit = dataset["Credit_Limit"].groupby(dataset[f"{eixoX}"]).mean()

        st.markdown(f"<h3 style='text-align: center;color: #d87093'>Gráfico interativo: Limite de crédito X {eixoX}</h3> ", unsafe_allow_html=True)
        feg = plt.figure(figsize=(15,7))
        sns.barplot(data=dataset, x=credit_limit.index, y=credit_limit.values,
        palette="Set2", dodge=False)
        plt.ylabel("Limite de crédito médio")
        plt.xlabel(f"{eixoX}")

        st.write("Esse gráfico permite a visualização do limite de crédito médio por coluna selecionada.")

        st.pyplot(feg)

        st.write("")
    
    elif graph == 'Clientes perdidos por coluna a ser selecionada':
        dataset = dataset.drop(['CLIENTNUM','Total_Relationship_Count', 'Total_Revolving_Bal', 'Avg_Open_To_Buy', 'Total_Amt_Chng_Q4_Q1', 'Total_Trans_Amt', 'Total_Trans_Ct', 'Total_Ct_Chng_Q4_Q1', 'Avg_Utilization_Ratio'], axis=1)

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

    elif graph == 'Gráfico de Caixa por coluna a ser selecionada':
        dataset = dataset.drop('CLIENTNUM', axis=1)
        eixoX = st.sidebar.selectbox("Selecione a coluna desejada:", dataset.select_dtypes(exclude='object').columns)

        st.write("Esse gráfico de caixa (boxplot) interativo permite a seleção de uma coluna do dataset para analisar a distribuição dos dados e a localização de outliers.\n\n Essa ferramenta é importante na análise exploratória de dados, pois mostra a distribuição dos dados, incluindo os valores mínimo e máximo, os quartis, a mediana e possíveis outliers.")
        st.markdown(f"<h3 style='text-align: center;color: #d87093'>Gráfico interativo: Clientes perdidos por {eixoX}</h3> ", unsafe_allow_html=True)
        sns.set(style='whitegrid')
        plt.figure(figsize=(8,6))

        sns.boxplot(x=eixoX, data=dataset, color='purple', saturation=0.7)
        plt.title(f"Gráfico de Caixa: {eixoX}")
        plt.title(f'Distribuição do {eixoX}', fontsize=16)
        plt.xlabel(f'{eixoX}', fontsize=14)
        plt.xticks(fontsize=12)

        st.pyplot()
        st.write("Ao analisarmos diferentes colunas com o gráfico de caixa, é possivel tirar algumas conclusões.")
        st.write("Considerando a análise dos gráficos de caixa de colunas como a de idade dos clientes e do tempo de relacionamento com o banco, por exemplo, as quais apresentam poucos outliers, optou-se por não excluir os outliers de colunas que apresentassem essa tendência, afinal como o número de outliers era baixo, não implicariam em mudanças significativas na análise exploratória dos dados.")
        st.write("Já se analisarmos os gráficos que apresentam bastante outliers, como a coluna de limite de crédito, também não foi feita a retirada dos outliers devido à impossibilidade de tratar essa grande quantidade de outliers sem influenciar no resultado da análise de dados.")
        st.write("Outro exemplo de gráfico de caixa que pode ser encontrado é o gráfico criado com número de dependentes, onde não foram identificados outliers, não sendo necessário nenhum tratamento.")

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