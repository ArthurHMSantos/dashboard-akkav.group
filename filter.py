import pandas as pd
import streamlit as st
from pandas.api.types import (
    is_categorical_dtype,
    is_datetime64_any_dtype,
    is_numeric_dtype,
    is_object_dtype,
)


def filter_dataset(dataset: pd.DataFrame) -> pd.DataFrame:
    """Filter a dataset using the sidebar."""
    modify = st.sidebar.checkbox("Adicionar filtros")

    if not modify:
        return dataset

    dataset = dataset.copy()

    # Try to convert datetimes into a standard format (datetime, no timezone)
    for col in dataset.columns:
        if is_object_dtype(dataset[col]):
            try:
                dataset[col] = pd.to_datetime(dataset[col])
            except Exception:
                pass

        if is_datetime64_any_dtype(dataset[col]):
            dataset[col] = dataset[col].dt.tz_localize(None)

    modification_container = st.sidebar.container()

    with modification_container:
        to_filter_columns = st.multiselect("Filtrar quadros com", dataset.columns)
        for column in to_filter_columns:
            left, right = st.columns((1, 23))
            # Treat columns with < 10 unique values as categorical
            if is_categorical_dtype(dataset[column]) or dataset[column].nunique() < 10:
                user_cat_input = right.multiselect(
                    f"Valores para {column}",
                    dataset[column].unique(),
                    default=list(dataset[column].unique()),
                )
                dataset = dataset[dataset[column].isin(user_cat_input)]
            elif is_numeric_dtype(dataset[column]):
                _min = float(dataset[column].min())
                _max = float(dataset[column].max())
                step = (_max - _min) / 100
                user_num_input = right.slider(
                    f"Valores para {column}",
                    min_value=_min,
                    max_value=_max,
                    value=(_min, _max),
                    step=step,
                )
                dataset = dataset[dataset[column].between(*user_num_input)]
            elif is_datetime64_any_dtype(dataset[column]):
                user_date_input = right.date_input(
                    f"Valores para {column}",
                    value=(
                        dataset[column].min(),
                        dataset[column].max(),
                    ),
                )
                if len(user_date_input) == 2:
                    user_date_input = tuple(map(pd.to_datetime, user_date_input))
                    start_date, end_date = user_date_input
                    dataset = dataset.loc[dataset[column].between(start_date, end_date)]
            else:
                user_text_input = right.text_input(
                    f"Substring or regex in {column}",
                )
                if user_text_input:
                    dataset = dataset[dataset[column].astype(str).str.contains(user_text_input)]

    return dataset

def filter_graphs(dataset: pd.DataFrame):
    st.sidebar.subheader("Filtros")
    gen = st.sidebar.checkbox("Genero", value=False)
    if gen:
        gen_options = dataset["Gender"].unique()
        gen = st.selectbox("Selecione o genero do cliente", gen_options)
        dataset = dataset[dataset["Gender"] == gen]
    age = st.sidebar.checkbox("Idade específica", value=False)
    if age:
        age_options = dataset["Customer_Age"].unique()
        age = st.select_slider("Selecione a idade do cliente: ", age_options)
        dataset = dataset[dataset["Customer_Age"] == age]

    edu = st.sidebar.checkbox("Nível de educação", value=False)
    if edu:
        edu_options = dataset["Education_Level"].unique()
        edu = st.selectbox("Selecione o Nível de Educação", edu_options)
        dataset = dataset[dataset["Education_Level"] == edu]
    catg = st.sidebar.checkbox("Categoria do cartão", value=False)
    if catg:
        card_options = dataset["Card_Category"].unique()
        card_type = st.selectbox('Selecione o tipo de cartão:', card_options)
        dataset = dataset[dataset["Card_Category"] == card_type]

    return dataset