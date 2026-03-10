@st.cache_resource
def train_model():

    df = pd.read_csv("data/housing.csv")

    df["rooms_per_household"] = df["total_rooms"] / df["households"]
    df["bedrooms_per_room"] = df["total_bedrooms"] / df["total_rooms"]
    df["population_per_household"] = df["population"] / df["households"]

    X = df.drop("median_house_value", axis=1)
    y = df["median_house_value"]

    from sklearn.ensemble import RandomForestRegressor

    model = RandomForestRegressor(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model

model = train_model()
