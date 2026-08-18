import streamlit as st
import pandas as pd
import utils

st.set_page_config(page_title="EV Sales Share Tracker", layout="wide")

st.title("📈 EV Sales Share Percentage Dashboard")
st.markdown("Track historical adoption milestones paired with continuous 2035 percentage projections.")
st.markdown("---")

try:
    data = utils.load_data()
    share_data = data[data['parameter'] == 'EV sales share']
    
    st.sidebar.header("Filter Configuration")
    all_countries = sorted([str(x) for x in share_data['region_country'].unique() if x != 'Unknown/Standard'])
    default_idx = all_countries.index('World') if 'World' in all_countries else 0
    selected_region = st.sidebar.selectbox("Select Country/Region", options=all_countries, index=default_idx)
    
    region_filtered = share_data[share_data['region_country'] == selected_region]
    all_modes = sorted([str(x) for x in region_filtered['mode'].unique() if x != 'Unknown/Standard'])
    selected_mode = st.sidebar.selectbox("Select Vehicle Mode", options=all_modes)
    
    final_filtered = region_filtered[region_filtered['mode'] == selected_mode]
    
    if not final_filtered.empty:
        final_filtered['value'] = pd.to_numeric(final_filtered['value'], errors='coerce').fillna(0)
        final_filtered['year'] = pd.to_numeric(final_filtered['year'], errors='coerce').fillna(0).astype(int)
        
        hist_df = final_filtered[final_filtered['category'] == 'Historical']
        proj_df = final_filtered[final_filtered['category'] != 'Historical']
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Historical Adoption Share (%)")
            if not hist_df.empty:
                chart_hist = hist_df.groupby(['year', 'powertrain'])['value'].sum().unstack(fill_value=0)
                st.line_chart(chart_hist)
            else:
                st.info("No historical observations recorded for this selection.")
                
        with col2:
            st.markdown("### 🔮 Long-Term 2035 Projections (%)")
            if not proj_df.empty:
                chart_proj = proj_df.groupby(['year', 'category'])['value'].sum().unstack(fill_value=0)
                st.line_chart(chart_proj)
            else:
                st.info("No projection models recorded for this selection.")
                
        st.markdown("---")
        st.markdown("#### 📋 Consolidated Data Matrix")
        st.dataframe(final_filtered[['year', 'category', 'powertrain', 'unit', 'value']], use_container_width=True, hide_index=True)
except Exception as e:
    st.error(f"Error executing sales share engine: {e}")
