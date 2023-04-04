import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="Dataset Infos",
    layout="wide",
    initial_sidebar_state="expanded",
)

def line_break():
    st.markdown('  ')

dataset = pd.read_csv("./assets/BankChurners.csv")

# Variáveis
existing_customer = dataset.where(dataset['Attrition_Flag'] == 'Existing Customer')
attrited_customer = dataset.where(dataset['Attrition_Flag'] == 'Attrited Customer')
male_existing_customer = existing_customer.where(dataset['Gender'] == 'M')
female_existing_customer = existing_customer.where(dataset['Gender'] == 'F')
male_attrited_customer = attrited_customer.where(dataset['Gender'] == 'M')
female_attrited_customer = attrited_customer.where(dataset['Gender'] == 'F')

st.markdown("<h1 style='text-align: center;color: #c9c904'>Dataset Infos</h1> ", unsafe_allow_html=True)
line_break()

# Quantidade M x F
st.markdown("<h3 style='color: #d87093;'>Quantidade</h3> ", unsafe_allow_html=True)
st.write('Número de clientes: ', existing_customer.value_counts().count())
st.write('(Masculino: ', male_existing_customer.value_counts().count(), ' | Feminino: ', female_existing_customer.value_counts().count(), ')')
st.write('Número de ex-clientes: ', attrited_customer.value_counts().count())
st.write('(Masculino: ', male_attrited_customer.value_counts().count(), ' | Feminino: ', female_attrited_customer.value_counts().count(), ')')
line_break()

# Escolaridade M x F
st.markdown("<h3 style='color: #d87093;text-align: center;'>Escolaridade</h3> ", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col2.caption('Clientes [Masculino]: ')
col2.write(dataset['Education_Level'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').value_counts())
col3.caption('Ex-clientes [Masculino]: ')
col3.write(dataset['Education_Level'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').value_counts())
col2.caption('Clientes [Feminino]: ')
col2.write(dataset['Education_Level'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').value_counts())
col3.caption('Ex-clientes [Feminino]: ')
col3.write(dataset['Education_Level'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').value_counts())
line_break()

# Estado civil M x F
st.markdown("<h3 style='color: #d87093;text-align: center;'>Estado Civil</h3> ", unsafe_allow_html=True)
col1, col2, col3, col4 = st.columns(4)
col2.caption('Clientes [Masculino]: ')
col2.write(dataset['Marital_Status'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').value_counts())
col3.caption('Ex-clientes [Masculino]: ')
col3.write(dataset['Marital_Status'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').value_counts())
col2.caption('Clientes [Feminino]: ')
col2.write(dataset['Marital_Status'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').value_counts())
col3.caption('Ex-clientes [Feminino]: ')
col3.write(dataset['Marital_Status'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').value_counts())
line_break()

# Limite de crédito M x F
st.markdown("<h3 style='color: #d87093;text-align: center;'>Limite de crédito</h3> ", unsafe_allow_html=True)
mean_m = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').mean()
median_m = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').median()
std_m = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').std()

ex_mean_m = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').mean()
ex_median_m = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').median()
ex_std_m = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').std()

mean_f = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').mean()
median_f = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').median()
std_f = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').std()

ex_mean_f = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').mean()
ex_median_f = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').median()
ex_std_f = dataset['Credit_Limit'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').std()

st.write('## Masculino ##')
st.write('#### Clientes')
st.markdown(f'* Média: ${mean_m:.2f}')
st.markdown(f'* Mediana: ${median_m:.2f}')
st.markdown(f'* Desvio Padrão: {std_m:.2f}')
st.write('#### Ex-clientes')
st.markdown(f'* Média: ${ex_mean_m:.2f}')
st.markdown(f'* Mediana: ${ex_median_m:.2f}')
st.markdown(f'* Desvio Padrão: {ex_std_m:.2f}')

st.write('## Feminino ##')
st.write('#### Clientes')
st.markdown(f'* Média: ${mean_f:.2f}')
st.markdown(f'* Mediana: ${median_f:.2f}')
st.markdown(f'* Desvio Padrão: {std_f:.2f}')
st.write('#### Ex-clientes')
st.markdown(f'* Média: ${ex_mean_f:.2f}')
st.markdown(f'* Mediana: ${ex_median_f:.2f}')
st.markdown(f'* Desvio Padrão: {ex_std_f:.2f}')

# Categoria do cartão M x F
st.markdown("<h3 style='color: #d87093;text-align: center;'>Categoria do cartão</h3> ", unsafe_allow_html=True)

cards_m = dataset['Card_Category'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').value_counts()
ex_cards_m = dataset['Card_Category'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').value_counts()

cards_f = dataset['Card_Category'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').value_counts()
ex_cards_f = dataset['Card_Category'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').value_counts()

col1, col2, col3, col4 = st.columns(4)
col2.caption('Clientes [Masculino]: ')
col2.write(cards_m)
col3.caption('Ex-clientes [Masculino]: ')
col3.write(ex_cards_m)
col2.caption('Clientes [Feminino]: ')
col2.write(cards_f)
col3.caption('Ex-clientes [Feminino]: ')
col3.write(ex_cards_f)
line_break()

# Período de relacionamento com o banco M x F
st.markdown("<h3 style='color: #d87093;text-align: center;'>Período de relacionamento com o banco (média)</h3> ", unsafe_allow_html=True)

months_m = dataset['Months_on_book'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').mean()
months_ex_m = dataset['Months_on_book'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').mean()

months_f = dataset['Months_on_book'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').mean()
months_ex_f = dataset['Months_on_book'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').mean()

col1, col2, col3, col4 = st.columns(4)
col2.caption('Clientes [Masculino]: ')
col2.write(f'{months_m:.2f}')
col3.caption('Ex-clientes [Masculino]: ')
col3.write(f'{months_ex_m:.2f}')
col2.caption('Clientes [Feminino]: ')
col2.write(f'{months_f:.2f}')
col3.caption('Ex-clientes [Feminino]: ')
col3.write(f'{months_ex_f:.2f}')
line_break()


# Renda anual
st.markdown("<h3 style='color: #d87093;text-align: center;'>Renda anual</h3> ", unsafe_allow_html=True)

income_m = dataset['Income_Category'].where(dataset['Gender'] == 'M').where(dataset['Attrition_Flag'] == 'Existing Customer').value_counts()
income_ex_m = dataset['Income_Category'].where(dataset['Gender'] == 'M').where(dataset['Gender'] == 'M').where(dataset['Attrition_Flag'] == 'Attrited Customer').value_counts()

income_f = dataset['Income_Category'].where(dataset['Gender'] == 'F').where(dataset['Attrition_Flag'] == 'Existing Customer').value_counts()
income_ex_f = dataset['Income_Category'].where(dataset['Gender'] == 'F').where(dataset['Attrition_Flag'] == 'Attrited Customer').value_counts()

col1, col2, col3, col4 = st.columns(4)
col2.caption('Clientes [Masculino]: ')
col2.write(income_m)
col3.caption('Ex-clientes [Masculino]: ')
col3.write(income_ex_m)
col2.caption('Clientes [Feminino]: ')
col2.write(income_f)
col3.caption('Ex-clientes [Feminino]: ')
col3.write(income_ex_f)
line_break()

# Dependentes
st.markdown("<h3 style='color: #d87093;text-align: center;'>Número de dependentes</h3> ", unsafe_allow_html=True)

relationship_m = dataset['Dependent_count'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'M').mean()
relationship_ex_m = dataset['Dependent_count'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'M').mean()

relationship_f = dataset['Dependent_count'].where(dataset['Attrition_Flag'] == 'Existing Customer').where(dataset['Gender'] == 'F').mean()
relationship_ex_f = dataset['Dependent_count'].where(dataset['Attrition_Flag'] == 'Attrited Customer').where(dataset['Gender'] == 'F').mean()

col1, col2, col3, col4 = st.columns(4)
col2.caption('Clientes [Masculino]: ')
col2.write(f'{relationship_m:.2f}')
col3.caption('Ex-clientes [Masculino]: ')
col3.write(f'{relationship_ex_m:.2f}')
col2.caption('Clientes [Feminino]: ')
col2.write(f'{relationship_f:.2f}')
col3.caption('Ex-clientes [Feminino]: ')
col3.write(f'{relationship_ex_f:.2f}')
line_break()
