import streamlit as st
import pandas as pd
import utils

st.set_page_config(page_title="EV Sales Tracker", layout="wide")
st.title("🚗 EV Sales (Historical & Projections)")
st.markdown("---")

try:
    data = utils.load_data()
    sales_data = data[data['parameter'] == 'EV sales']
    
    all_countries = sorted([str(x) for x in sales_data['region_country'].unique() if x != 'Unknown/Standard'])
    default_idx = all_countries.index('World') if 'World' in all_countries else 0
    selected_region = st.sidebar.selectbox("Select Country/Region", options=all_countries, index=default_idx)
    
    region_filtered = sales_data[sales_data['region_country'] == selected_region]
    all_modes = sorted([str(x) for x in region_filtered['mode'].unique() if x != 'Unknown/Standard'])
    selected_mode = st.sidebar.selectbox("Select Vehicle Mode", options=all_modes)
    
    final_filtered = region_filtered[region_filtered['mode'] == selected_mode]
    
    if not final_filtered.empty:
        final_filtered['value'] = pd.to_numeric(final_filtered['value'], errors='coerce').fillna(0)
        final_filtered['year'] = pd.to_numeric(final_filtered['year'], errors='coerce').fillna(0).astype(int)
        
        chart_data = final_filtered.groupby(['year', 'category'])['value'].sum().unstack(fill_value=0)
        st.line_chart(chart_data)
        st.dataframe(final_filtered[['year', 'category', 'powertrain', 'unit', 'value']], use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error: {e}")
