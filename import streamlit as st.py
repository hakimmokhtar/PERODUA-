import streamlit as st
import pandas as pd
from PIL import Image
import os

st.set_page_config(page_title="Perodua Car Models", layout="wide")

# Load data
df = pd.read_csv("data/perodua_models.csv")

st.title("🚗 Senarai Model Perodua")
st.markdown("Banding, tapis dan lihat maklumat penuh kereta Perodua.")

# Sidebar Filters
st.sidebar.header("🔍 Tapis Model")
engine_filter = st.sidebar.multiselect("Kapasiti Enjin", options=df["Engine"].unique())
fuel_filter = st.sidebar.multiselect("Jenis Bahan Api", options=df["FuelType"].unique())
price_range = st.sidebar.slider("Julat Harga (RM)", int(df.Price.min()), int(df.Price.max()), (int(df.Price.min()), int(df.Price.max())))

# Apply filters
filtered_df = df[
    (df["Price"] >= price_range[0]) & 
    (df["Price"] <= price_range[1])
]

if engine_filter:
    filtered_df = filtered_df[filtered_df["Engine"].isin(engine_filter)]
if fuel_filter:
    filtered_df = filtered_df[filtered_df["FuelType"].isin(fuel_filter)]

# Search Box
search = st.text_input("Cari Model")
if search:
    filtered_df = filtered_df[filtered_df["Model"].str.contains(search, case=False)]

# Show Filtered Models
st.subheader("📋 Senarai Model")
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

# Compare Models
st.subheader("🔄 Bandingkan Model")
selected_models = st.multiselect("Pilih model untuk dibandingkan", options=df["Model"].tolist())
if len(selected_models) >= 2:
    compare_df = df[df["Model"].isin(selected_models)].set_index("Model")
    st.table(compare_df.drop(columns=["Image"]))
