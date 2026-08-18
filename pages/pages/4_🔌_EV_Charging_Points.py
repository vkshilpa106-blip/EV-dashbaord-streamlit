import streamlit as st
import pandas as pd
import utils

st.set_page_config(page_title="EV Charging Points Tracker", layout="wide")

st.title("🔌 EV Charging Points Infrastructure Dashboard")
st.markdown("Track public infrastructure development timelines paired with continuous 2035 networks expansion projections.")
st.markdown("---")

try:
    data = utils.load_data()
    charging_data = data[data['parameter'] == 'EV charging points']
    
    st.sidebar.header("Filter Configuration")
    all_countries = sorted([str(x) for x in charging_data['region_country'].unique() if x != 'Unknown/Standard'])
    default_idx = all_countries.index('World') if 'World' in all_countries else 0
    selected_region = st.sidebar.selectbox("Select Country/Region", options=all_countries, index=default_idx)
    
    # Slicing explicitly by location (Skipping mode checks entirely to resolve empty data blocks)
    final_filtered = charging_data[charging_data['region_country'] == selected_region]
    
    if not final_filtered.empty:
        final_filtered['value'] = pd.to_numeric(final_filtered['value'], errors='coerce').fillna(0)
        final_filtered['year'] = pd.to_numeric(final_filtered['year'], errors='coerce').fillna(0).astype(int)
        
        hist_df = final_filtered[final_filtered['category'] == 'Historical']
        proj_df = final_filtered[final_filtered['category'] != 'Historical']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Historical Network Stations Installed")
            if not hist_df.empty:
                # Group charging stations by speed type (Fast vs Slow networks)
                chart_hist = hist_df.groupby(['year', 'powertrain'])['value'].sum().unstack(fill_value=0)
                st.line_chart(chart_hist)
            else:
                st.info("No historical observations recorded for this selection.")
                
        with col2:
            st.markdown("### 🔮 Long-Term Infrastructure Projections")
            if not proj_df.empty:
                chart_proj = proj_df.groupby(['year', 'category'])['value'].sum().unstack(fill_value=0)
                st.line_chart(chart_proj)
            else:
                st.info("No projection infrastructure maps recorded for this selection.")
                
        st.markdown("---")
        st.markdown("#### 📋 Consolidated Infrastructure Data Matrix")
        st.dataframe(final_filtered[['year', 'category', 'powertrain', 'unit', 'value']], use_container_width=True, hide_index=True)
    else:
        st.warning("⚠️ No recorded charging infrastructure entries found for this region selection.")
except Exception as e:
    st.error(f"Error executing infrastructure charging points engine: {e}")
