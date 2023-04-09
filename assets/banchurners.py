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

    # Test the classifier with new data
    # print("ESPERADOS: 5 EXISTING")
    # user2 = [43, 'F', 4, 'High School', 'Unknown', 'Less than $40K', 'Blue', 2786, 39, 993, 0.644]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # # wait :  existing
    # user2 = [41, 'F', 3, 'College', 'Married', 'Less than $40K', 'Blue', 1438.3, 37, 673.3, 0.532]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # user2 = [32,"M",0,"High School","Unknown","$80K - $120K","Blue",15412, 36, 15412, 0.0]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # user2 = [45,"M",2,"Graduate","Married","Unknown","Platinum", 34516, 31, 33208, 0.0380]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # user2 = [56,"F",1,"High School","Single","$60K - $80K","Blue", 13940, 34, 11831, 0.151]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)


    # print("ESPERADOS: 5 ATTRITED")

    # user2 = [62, 'F', 0, "Graduate", "Married", "Less than $40K", "Blue", 1438.3, 49, 1438.3, 0.0] 
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # user2 = [26,"F",0,"High School","Single","$40K - $60K","Blue", 1730, 13, 114.0, 0.9340]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # user2 = [46, "F", 3, "Graduate", "Single", "Less than $40K", "Blue", 8551, 28, 7484, 0.125]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # user2 = [39,"M",2,"Uneducated","Single","$60K - $80K","Blue", 13961, 29, 2187, 0.0]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    # user2 = [34,"F",3,"Graduate","Married","Less than $40K","Gold", 15487, 36, 13640, 0.119]
    # user_input = preprocess_user_input(user2, scaler, le,le_gender, le_education, le_cat, le_card)
    # state = predict_churn(user_input, rfc)
    # print("Predicted State: ", state)

    return state