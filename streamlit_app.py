import pandas as pd
import streamlit as st
from sklearn.ensemble import RandomForestRegressor

st.set_page_config(page_title="California House Price Predictor", layout="centered")

st.title("California House Price Predictor")
st.write("Enter housing details and get a predicted median house value.")

@st.cache_resource
def train_model():
    df = pd.read_csv("housing.csv")

    df["rooms_per_household"] = df["total_rooms"] / df["households"]
    df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"]
    df["population_per_household"] = df["population"] / df["households"]

    X = df.drop("median_house_value", axis=1)
    y = df["median_house_value"]

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )
    model.fit(X, y)
    return model

model = train_model()

st.subheader("Input features")

longitude = st.number_input("Longitude", value=-122.23, format="%.2f")
latitude = st.number_input("Latitude", value=37.88, format="%.2f")
housing_median_age = st.number_input("Housing median age", min_value=1.0, value=41.0)
total_rooms = st.number_input("Total rooms", min_value=1.0, value=880.0)
total_bedrooms = st.number_input("Total bedrooms", min_value=1.0, value=129.0)
population = st.number_input("Population", min_value=1.0, value=322.0)
households = st.number_input("Households", min_value=1.0, value=126.0)
median_income = st.number_input("Median income", min_value=0.0, value=8.3252, format="%.4f")

if st.button("Predict house price"):
    rooms_per_household = total_rooms / households if households else 0
    bedrooms_per_room = total_bedrooms / total_rooms if total_rooms else 0
    population_per_household = population / households if households else 0

    input_df = pd.DataFrame([{
        "longitude": longitude,
        "latitude": latitude,
        "housing_median_age": housing_median_age,
        "total_rooms": total_rooms,
        "total_bedrooms": total_bedrooms,
        "population": population,
        "households": households,
        "median_income": median_income,
        "rooms_per_household": rooms_per_household,
        "bedrooms_per_room": bedrooms_per_room,
        "population_per_household": population_per_household
    }])

    prediction = model.predict(input_df)[0]
    st.metric("Predicted median house value", f"${prediction:,.0f}")

    with st.expander("See engineered features"):
        st.write({
            "rooms_per_household": rooms_per_household,
            "bedrooms_per_room": bedrooms_per_room,
            "population_per_household": population_per_household
        })