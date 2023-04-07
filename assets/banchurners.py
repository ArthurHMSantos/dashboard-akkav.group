import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import warnings
warnings.filterwarnings("ignore")
from sklearn.model_selection import train_test_split
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
from imblearn.over_sampling import SMOTE
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import GridSearchCV

def predicting_churn(user_input):
    df = pd.read_csv("assets/BankChurners.csv")
    df.drop_duplicates(inplace=True)
    cols_to_use = ["Attrition_Flag", "Customer_Age", "Gender", "Dependent_count", "Education_Level", "Marital_Status", "Income_Category", "Card_Category", "Credit_Limit", "Months_on_book", "Avg_Open_To_Buy", "Avg_Utilization_Ratio"]
    df = df[cols_to_use]

    le = LabelEncoder()
    df["Attrition_Flag"] = le.fit_transform(df["Attrition_Flag"])
    le_gender = LabelEncoder()
    df["Gender"] = le_gender.fit_transform(df["Gender"])
    le_education = LabelEncoder()
    df["Education_Level"] = le_education.fit_transform(df["Education_Level"])
    df["Marital_Status"] = le.fit_transform(df["Marital_Status"])
    le_cat = LabelEncoder()
    df["Income_Category"] = le_cat.fit_transform(df["Income_Category"])
    le_card = LabelEncoder()
    df["Card_Category"] = le_card.fit_transform(df["Card_Category"])

    x = df.drop("Attrition_Flag", axis=1) 
    y = df["Attrition_Flag"] # Target variable
    x_train, x_test, y_train, y_test = train_test_split(x, y, train_size=0.7, random_state=45)

    scaler = StandardScaler()
    x_train = scaler.fit_transform(x_train)
    x_test = scaler.transform(x_test)

    smote = SMOTE(random_state=42)
    x_train, y_train = smote.fit_resample(x_train, y_train)

    rfc = RandomForestClassifier(random_state=42)
    rfc.fit(x_train, y_train)

    y_pred = rfc.predict(x_test)
    print("Accuracy Score: ", accuracy_score(y_test, y_pred))
    print("Classification Report: ", classification_report(y_test, y_pred))

    def preprocess_user_input(user_input, scaler, le, le_gender, le_edu, le_cat, le_card):
        user_input_df = pd.DataFrame([user_input], columns=cols_to_use[1:])
        user_input_df["Gender"] = le_gender.transform(user_input_df["Gender"])
        user_input_df["Education_Level"] = le_edu.transform(user_input_df["Education_Level"])
        user_input_df["Marital_Status"] = le.transform(user_input_df["Marital_Status"])
        user_input_df["Income_Category"] = le_cat.transform(user_input_df["Income_Category"])
        user_input_df["Card_Category"] = le_card.transform(user_input_df["Card_Category"])
        if "Attrition_Flag" in user_input_df.columns:
            print("Dropping Attrition_Flag...")
            user_input_df = user_input_df.drop("Attrition_Flag", axis=1)
        user_input_scaled = scaler.transform(user_input_df)
        return user_input_scaled

    def predict_churn(user_input, model):
        prediction = model.predict(user_input)
        return "Existing" if prediction[0] == 1 else "Attrited"

    user_input_scaled = preprocess_user_input(user_input, scaler, le, le_gender, le_education, le_cat, le_card)
    state = predict_churn(user_input_scaled, rfc)

    return state