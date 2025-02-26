
import streamlit as st
import pandas as pd
from utils_rent_price_pridiction import load_data, predict_rent, analyze_data
def main():
    st.title("Rent Price Prediction App")
st.write("This app predicts the rent price of an apartment based on the square footage, number of bedrooms, bathrooms, city, state, and amenities.")
df = load_data()


st.write("Enter details to predict rent price")

square_feet = st.number_input("Square Footage", min_value=0.0, value=500.0)
bedrooms = st.number_input("Bedrooms", min_value=0, value=1)
bathrooms = st.number_input("Bathrooms", min_value=0, value=1)
cityname = st.selectbox("City", df["cityname"].unique())
state = st.selectbox("State", df["state"].unique())
amenities = st.multiselect("Amenities", df["amenities"].dropna().unique())

if st.button("Predict Rent Price"):
    data = pd.DataFrame([[square_feet, bedrooms, bathrooms, cityname, state, ','.join(amenities)]], 
                        columns=["square_feet", "bedrooms", "bathrooms", "cityname", "state", "amenities"])
    # Ensure numerical columns are float
    data[["square_feet", "bedrooms", "bathrooms"]] = data[["square_feet", "bedrooms", "bathrooms"]].astype(float)
    prediction = predict_rent(data)
    st.write(f"Predicted Rent Price: ${prediction[0]:,.2f}")

# Show Data Analysis
analyze_data(df)

if __name__ == "__main__":
    main()