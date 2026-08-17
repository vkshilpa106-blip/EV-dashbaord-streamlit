import streamlit as st

import utils

st.set_page_config(page_title="🌍 Global EV Dashboard", layout="wide")

st.title("🌍 Global EV Dashboard")

df = utils.load_clean_data()

countries = sorted(df["region_country"].dropna().unique())
selected_country = st.sidebar.selectbox("Select country / region", countries)

filtered_df = df[df["region_country"] == selected_country].sort_values(
    ["parameter", "year", "mode"]
)

st.subheader(f"Data for {selected_country}")
st.dataframe(filtered_df, use_container_width=True, hide_index=True)
