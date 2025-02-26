from turtle import st
import pandas as pd
import numpy as np
import joblib
import os
import seaborn as sns
import matplotlib.pyplot as plt
import streamlit as st
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.ensemble import RandomForestRegressor


def load_data():
    file_path = r"D:\agenticAI_portolio\apartments_for_rent_classified_100K.csv"
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Dataset not found at {file_path}. Please ensure it is downloaded.")
    
    df = pd.read_csv(file_path, delimiter=';', encoding='ISO-8859-1')
    df = df[["square_feet", "bedrooms", "bathrooms", "amenities", "cityname", "state", "price"]]
    df.dropna(inplace=True)
    return df

def analyze_data(df):
    summary_stats = df.describe()
    
    # Display statistics on UI
    st.subheader("Summary Statistics")
    st.write(summary_stats)
    
    # Visualizations
    # st.subheader("Data Distributions")
    # fig, ax = plt.subplots(figsize=(10, 6))
    # sns.histplot(df["price"], bins=50, kde=True, ax=ax)
    # ax.set_title("Price Distribution")
    # st.pyplot(fig)
    # plt.close(fig)
    
    # fig, ax = plt.subplots(figsize=(10, 6))
    # sns.scatterplot(x=df["square_feet"], y=df["price"], alpha=0.5, ax=ax)
    # ax.set_title("Square Feet vs Price")
    # ax.set_xlabel("Square Feet")
    # ax.set_ylabel("Price")
    # st.pyplot(fig)

def train_model(df):
    analyze_data(df)  # Perform data analysis before training
    X = df.drop(columns=["price"])
    y = df["price"]
    categorical_features = ["cityname", "state", "amenities"]
    numerical_features = ["square_feet", "bedrooms", "bathrooms"]
    
    categorical_transformer = OneHotEncoder(handle_unknown='ignore')
    numerical_transformer = StandardScaler()
    preprocessor = ColumnTransformer([
        ('num', numerical_transformer, numerical_features),
        ('cat', categorical_transformer, categorical_features)
    ])
    
    model = Pipeline([
        ('preprocessor', preprocessor),
        ('regressor', RandomForestRegressor(n_estimators=100, random_state=42))
    ])
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, "rent_price_model.pkl")

def predict_rent(data):
    model_path = "rent_price_model.pkl"
    if not os.path.exists(model_path):
        df = load_data()
        train_model(df)
    model = joblib.load(model_path)
    return model.predict(data)