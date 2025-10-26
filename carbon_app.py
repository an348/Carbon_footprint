import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt

# Load trained model and features
model = joblib.load("carbon_model.pkl")
feature_cols = joblib.load("model_features.pkl")

st.set_page_config(page_title="Carbon Footprint Awareness", page_icon="🌿", layout="wide")

# 🌳 Background styling
page_bg = """
<style>
[data-testid="stAppViewContainer"] {
    background-image: url("https://img.freepik.com/free-photo/misty-forest-landscape_181624-44201.jpg");
    background-size: cover;
    background-position: center;
    background-attachment: fixed;
}

[data-testid="stHeader"] {background: rgba(0,0,0,0);}
div.block-container {
    background-color: rgba(255,255,255,0.88);
    border-radius: 20px;
    padding: 2rem;
    margin-top: 2rem;
}
</style>
"""
st.markdown(page_bg, unsafe_allow_html=True)

# 🌍 Navigation control
if "page" not in st.session_state:
    st.session_state.page = "awareness" 

# 🏞️ PAGE 1: Awareness Section
if st.session_state.page == "awareness":
    st.markdown(
        """
        <h1 style='text-align:center; color:#2E8B57;'>🌿 About Carbon Footprint</h1>
        <p style='font-size:18px; text-align:justify;'>
        A <b>carbon footprint</b> measures the total greenhouse gas emissions produced by human activities —
        from driving 🚗 and flying ✈️ to energy use ⚡ and food consumption 🍔. 
        It helps us understand how our everyday choices impact the planet 🌎.
        </p>

        <h2 style='color:#2E8B57;'>🌱 Why It Matters</h2>
        <ul style='font-size:17px;'>
            <li><b>🌤️ Climate Impact:</b> Reducing emissions helps fight global warming and extreme weather.</li>
            <li><b>💧 Resource Conservation:</b> Saves energy, water, and raw materials.</li>
            <li><b>🌿 Sustainable Living:</b> Encourages eco-friendly habits and mindful consumption.</li>
            <li><b>🧘 Health and Well-being:</b> Promotes cleaner air and a healthier planet for all.</li>
        </ul>
        """,
        unsafe_allow_html=True
    )

    # Centered button
    st.markdown(
        """
        <style>
        .center-button {
            display: flex;
            justify-content: center;
            align-items: center;
            margin-top: 20px;
        }
        .check-btn {
            background-color: #2E8B57;
            color: white;
            border: none;
            padding: 18px 35px;
            border-radius: 50px;
            font-size: 22px;
            font-weight: bold;
            cursor: pointer;
            transition: 0.3s;
            box-shadow: 0px 6px 12px rgba(0, 100, 0, 0.4);
        }
        .check-btn:hover {
            background-color: #1f6d44;
            transform: scale(1.05);
            box-shadow: 0px 8px 16px rgba(0, 100, 0, 0.5);
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    if st.button("🌍 Check Your Carbon Footprint"):
        st.session_state.page = "input"
        st.rerun()

# -----------------------------------------------------------
# 📋 PAGE 2: Input Form
elif st.session_state.page == "input":
    st.markdown("<h2 style='text-align:center; color:#2E8B57;'>Enter Your Daily Habits</h2>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        vehicle_distance = st.slider("Vehicle monthly distance (km)", 0, 10000, 1000)
        air_freq = st.selectbox("Frequency of traveling by air",
                                ["never", "rarely", "frequently", "very frequently"])
        vehicle_type = st.selectbox("Vehicle type",
                                    ["No Vehicle", "petrol", "diesel", "hybrid", "lpg", "electric"])
        sex = st.selectbox("Gender", ["female", "male"])

    with col2:
        body_type = st.selectbox("Body Type", ["underweight", "normal", "overweight", "obese"])
        new_clothes = st.slider("How many new clothes do you buy monthly?", 0, 50, 5)
        waste_bag_count = st.slider("Waste bags used weekly", 0, 20, 4)
        waste_bag_size = st.selectbox("Waste bag size", ["small", "medium", "large", "extra large"])
        diet = st.multiselect("Diet type", ["pescatarian", "vegan", "vegetarian","omnivore"])

    # Encoding user input
    body_map = {'underweight': 1, 'normal': 2, 'overweight': 3, 'obese': 4}
    air_map = {'never': 1, 'rarely': 2, 'frequently': 3, 'very frequently': 4}
    waste_size_map = {'small': 1, 'medium': 2, 'large': 3, 'extra large': 4}

    sex_male = 1 if sex == "male" else 0
    vehicle_petrol = 1 if vehicle_type == "petrol" else 0
    vehicle_diesel = 1 if vehicle_type == "diesel" else 0
    vehicle_hybrid = 1 if vehicle_type == "hybrid" else 0
    vehicle_lpg = 1 if vehicle_type == "lpg" else 0
    vehicle_electric = 1 if vehicle_type == "electric" else 0

    diet_pescatarian = 1 if "pescatarian" in diet else 0
    diet_vegan = 1 if "vegan" in diet else 0
    diet_vegetarian = 1 if "vegetarian" in diet else 0

    user_data = pd.DataFrame([[ 
        vehicle_distance,
        air_map[air_freq],
        vehicle_petrol,
        vehicle_lpg,
        vehicle_diesel,
        body_map[body_type],
        new_clothes,
        sex_male,
        waste_bag_count,
        waste_size_map[waste_bag_size],
        vehicle_hybrid,
        vehicle_electric,
        diet_pescatarian,
        diet_vegan,
        diet_vegetarian
    ]], columns=feature_cols)

    # Green circular prediction button
    st.markdown("""
        <style>
        .predict-row {
            display: flex;
            align-items: center;
            margin-top: 20px;
            margin-bottom: 25px;
        }
        div.stButton > button:first-child {
            background-color: #00B050;
            color: white;
            border: none;
            padding: 30px 33px;
            border-radius: 50%;
            font-size: 50px;
            font-weight: bold;
            box-shadow: 0px 6px 15px rgba(0, 128, 0, 0.5);
            transition: 0.3s;
            margin-left: 150px;
        }
        div.stButton > button:hover {
            background-color: #009933;
            transform: scale(1.1);
            box-shadow: 0px 8px 18px rgba(0, 128, 0, 0.6);
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown("<div class='predict-row'>", unsafe_allow_html=True)
    btn_clicked = st.button("👣")
    st.markdown("<h4 style='color:#006400; margin-left:20px;'>Check your burden on Earth 😉🌍</h4>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if btn_clicked:
        st.session_state.page = "result"
        st.session_state.user_data = user_data
        st.rerun()

# 📊 PAGE 3: Result + Pie Chart
elif st.session_state.page == "result":
    user_data = st.session_state.user_data
    prediction = model.predict(user_data)[0]

    st.success(f"### 🌱 Your estimated annual carbon emission: **{prediction:.2f} kg CO₂/year**")

    avg_emission = 2800
    if prediction > avg_emission:
        st.warning(f"⚠️ Your footprint is {prediction - avg_emission:.2f} kg higher than average.")
    else:
        st.info(f"✅ You are {avg_emission - prediction:.2f} kg lower than average.")

    categories = ["Travel", "Diet", "Waste", "Lifestyle"]
    contributions = [40, 25, 20, 15]

    fig, ax = plt.subplots(figsize=(1.5, 1.5))
    ax.pie(
        contributions,
        labels=categories,
        autopct='%1.1f%%',
        startangle=90,
        textprops={'fontsize': 4},
        wedgeprops={'edgecolor': 'white'}
    )
    ax.set_title("Your Carbon Footprint Breakdown", fontsize=12, pad=10)
    st.markdown("<div style='text-align: center;'>", unsafe_allow_html=True)
    st.pyplot(fig)
    st.markdown("</div>", unsafe_allow_html=True)

    # 💡 Insights
    st.markdown("<h4 style='color:#2E8B57;'>💡 Insights</h4>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;'>🚗 Travel and diet account for most CO₂ emissions.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;'>🌿 Switching to public or hybrid transport can cut emissions by ~20%.</p>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:13px;'>👕 Buying fewer clothes and reducing waste lowers emissions significantly.</p>", unsafe_allow_html=True)

    if st.button("⬅️ Go Back to Awareness Page"):
        st.session_state.page = "awareness"
        st.rerun()
