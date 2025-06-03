import streamlit as st
import json
import os
from PIL import Image
import pandas as pd

st.set_page_config(page_title="Perodua Car Finder", layout="wide")

# Tajuk Aplikasi
st.title('PENCARIAN ENGINEER DAFFIM SDN BHD!! 🚗')
st.write('Selamat datang ke portal carian model kereta Perodua.')

# Input mesej pengguna
user_input = st.text_input('Masukkan mesej tersuai:', 'Saya nak beli kereta Perodua!')
st.write('Mesej Anda:', user_input)

st.markdown("---")
st.header("📋 Senarai Model Perodua")

# Fungsi untuk baca data JSON
@st.cache_data
def get_perodua_models():
    with open("data/perodua_models.json") as f:
        return json.load(f)

# Dapatkan data model
models_data = get_perodua_models()
model_names = [model["Model"] for model in models_data]

# Pilih model secara dropdown
selected_model = st.selectbox("Pilih model kereta:", ["-- Sila pilih --"] + model_names)

# Tapis model terpilih
if selected_model != "-- Sila pilih --":
    model = next((m for m in models_data if m["Model"] == selected_model), None)
    if model:
        col1, col2 = st.columns([1, 2])
        with col1:
            img_path = os.path.join("images", model["Image"])
            if os.path.exists(img_path):
                st.image(Image.open(img_path), width=250)
            else:
                st.warning("Gambar tidak dijumpai")
        with col2:
            st.subheader(f"Maklumat {model['Model']}")
            st.markdown(f"- **Enjin:** {model['Engine']}")
            st.markdown(f"- **Bahan Api:** {model['FuelType']}")
            st.markdown(f"- **Harga:** RM {model['Price']:,}")
            st.markdown(f"- **Saiz:** {model['Size']}")
        st.markdown("---")

# Perbandingan model
st.subheader("📊 Bandingkan Model")
selected_models = st.multiselect("Pilih model untuk dibandingkan", options=model_names)
if len(selected_models) >= 2:
    compare_data = [m for m in models_data if m["Model"] in selected_models]
    st.table(pd.DataFrame(compare_data).drop(columns=["Image"]))
