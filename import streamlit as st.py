import streamlit as st
import json
import os
from PIL import Image
import requests

st.set_page_config(page_title="Perodua Car Finder", layout="wide")

# Tajuk Aplikasi
st.title('PENCARIAN ENGINEER DAFFIM SDN BHD!! 🚗')
st.write('Selamat datang ke portal carian model kereta Perodua.')

# Input mesej pengguna
user_input = st.text_input('Enter a custom message:', 'Hello, Streamlit!')
st.write('Customized Message:', user_input)

# Currency API
try:
    response = requests.get('https://api.vatcomply.com/rates?base=MYR')
    if response.status_code == 200:
        data = response.json()
        rates = data.get('rates', {})
        selected_currency = st.selectbox('Convert MYR to:', sorted(rates.keys()))
        amount_myr = st.number_input('Amount in MYR:', min_value=0.0, value=1.0, step=0.1)
        if selected_currency and amount_myr:
            converted_amount = amount_myr * rates[selected_currency]
            st.success(f"{amount_myr:.2f} MYR = {converted_amount:.2f} {selected_currency}")
    else:
        st.warning("Currency API not available.")
except:
    st.warning("Connection issue for currency exchange.")

st.markdown("---")
st.header("📋 Senarai Model Perodua")

# Fungsi untuk baca data JSON (seolah-olah dari API)
@st.cache_data
def get_perodua_models():
    with open("data/perodua_models.json") as f:
        return json.load(f)

# Dapatkan data model
models_data = get_perodua_models()

# Sidebar untuk tapis
st.sidebar.header("🔍 Tapisan")
engine_options = list(set([m["Engine"] for m in models_data]))
fuel_options = list(set([m["FuelType"] for m in models_data]))

engine_filter = st.sidebar.multiselect("Jenis Enjin", engine_options)
fuel_filter = st.sidebar.multiselect("Jenis Bahan Api", fuel_options)

min_price = min(m["Price"] for m in models_data)
max_price = max(m["Price"] for m in models_data)
price_range = st.sidebar.slider("Julat Harga (RM)", min_price, max_price, (min_price, max_price))

# Penapis
filtered_models = []
for model in models_data:
    if engine_filter and model["Engine"] not in engine_filter:
        continue
    if fuel_filter and model["FuelType"] not in fuel_filter:
        continue
    if not (price_range[0] <= model["Price"] <= price_range[1]):
        continue
    filtered_models.append(model)

# Carian
search_term = st.text_input("🔎 Cari model:")
if search_term:
    filtered_models = [m for m in filtered_models if search_term.lower() in m["Model"].lower()]

# Papar hasil
for model in filtered_models:
    col1, col2 = st.columns([1, 2])
    with col1:
        img_path = os.path.join("images", model["Image"])
        if os.path.exists(img_path):
            st.image(Image.open(img_path), width=200)
        else:
            st.text("Tiada gambar")
    with col2:
        st.markdown(f"### {model['Model']}")
        st.markdown(f"- Enjin: {model['Engine']}")
        st.markdown(f"- Bahan Api: {model['FuelType']}")
        st.markdown(f"- Harga: RM {model['Price']:,}")
        st.markdown(f"- Saiz: {model['Size']}")
    st.markdown("---")

# Perbandingan
st.subheader("📊 Bandingkan Model")
selected_models = st.multiselect("Pilih model untuk dibandingkan", options=[m["Model"] for m in models_data])
if len(selected_models) >= 2:
    compare_data = [m for m in models_data if m["Model"] in selected_models]
    st.table(pd.DataFrame(compare_data).drop(columns=["Image"]))


