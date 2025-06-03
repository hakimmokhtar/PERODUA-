import streamlit as st
import pandas as pd
import os
from PIL import Image
import requests

# Tajuk Aplikasi
st.title('PENCARIAN ENGINEER DAFFIM SDN BHD!!')
st.write('Welcome to DAFFIM SDN BHD!')

# Input mesej pengguna
widgetuser_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('Customized Message:', widgetuser_input)

# Tambahan: Currency Exchange API
response = requests.get('https://api.vatcomply.com/rates?base=MYR')
if response.status_code == 200:
    data = response.json()
    rates = data.get('rates', {})
    selected_currency = st.selectbox('Convert MYR to:', sorted(rates.keys()))
    amount_myr = st.number_input('Enter amount in MYR:', min_value=0.0, value=1.0, step=0.1)
    if selected_currency and amount_myr:
        converted_amount = amount_myr * rates[selected_currency]
        st.success(f"{amount_myr:.2f} MYR = {converted_amount:.2f} {selected_currency}")
else:
    st.error("Currency API failed.")

st.markdown("---")
st.header("🚗 Senarai Model Kereta Perodua")

# Load data CSV
df = pd.read_csv("data/perodua_models.csv")

# Sidebar: Penapis
st.sidebar.header("🔍 Tapis Model")
engine_filter = st.sidebar.multiselect("Kapasiti Enjin", options=df["Engine"].unique())
fuel_filter = st.sidebar.multiselect("Jenis Bahan Api", options=df["FuelType"].unique())
price_range = st.sidebar.slider("Julat Harga (RM)", int(df.Price.min()), int(df.Price.max()), (int(df.Price.min()), int(df.Price.max())))

# Tapisan data
filtered_df = df[
    (df["Price"] >= price_range[0]) & 
    (df["Price"] <= price_range[1])
]
if engine_filter:
    filtered_df = filtered_df[filtered_df["Engine"].isin(engine_filter)]
if fuel_filter:
    filtered_df = filtered_df[filtered_df["FuelType"].isin(fuel_filter)]

# Carian model
search = st.text_input("Cari model kereta:")
if search:
    filtered_df = filtered_df[filtered_df["Model"].str.contains(search, case=False)]

# Paparan model
for i, row in filtered_df.iterrows():
    col1, col2 = st.columns([1, 2])
    with col1:
        img_path = os.path.join("images", row["Image"])
        if os.path.exists(img_path):
            st.image(Image.open(img_path), width=200)
        else:
            st.text("Tiada gambar")
    with col2:
        st.markdown(f"### {row['Model']}")
        st.markdown(f"- Enjin: {row['Engine']}")
        st.markdown(f"- Bahan Api: {row['FuelType']}")
        st.markdown(f"- Harga: RM {row['Price']:,}")
        st.markdown(f"- Saiz: {row['Size']}")
    st.markdown("---")

# Fungsi banding model
st.subheader("🔄 Bandingkan Model")
selected_models = st.multiselect("Pilih model untuk dibandingkan", options=df["Model"].tolist())
if len(selected_models) >= 2:
    compare_df = df[df["Model"].isin(selected_models)].set_index("Model")
    st.table(compare_df.drop(columns=["Image"]))
