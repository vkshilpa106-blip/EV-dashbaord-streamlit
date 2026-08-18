import streamlit as st
import pandas as pd
import utils

# 1. Establish Page View Layout Configuration
st.set_page_config(page_title="EV Charging Points Tracker", layout="wide")

st.title("🔌 EV Charging Points Infrastructure Dashboard")
st.markdown("Track public infrastructure development timelines paired with continuous 2035 network expansion projections.")
st.markdown("---")

try:
    # 2. Ingest Data Matrix
    data = utils.load_data()
    
    # Isolate specifically the EV charging points parameter rows across all timeline horizons
    charging_data = data[data['parameter'] == 'EV charging points']
    
    # 3. Sidebar Filter Configurations Input Column Layer
    st.sidebar.header("Filter Configuration")
    all_countries = sorted([str(x) for x in charging_data['region_country'].unique() if x != 'Unknown/Standard'])
    default_idx = all_countries.index('World') if 'World' in all_countries else 0
    selected_region = st.sidebar.selectbox("Select Country/Region", options=all_countries, index=default_idx)
    
    # Filter dataset down explicitly to the target location region
    final_filtered = charging_data[charging_data['region_country'] == selected_region]
    
    if not final_filtered.empty:
        # Secure explicit numerical properties safely to avoid mapping errors
        final_filtered['value'] = pd.to_numeric(final_filtered['value'], errors='coerce').fillna(0)
        final_filtered['year'] = pd.to_numeric(final_filtered['year'], errors='coerce').fillna(0).astype(int)
        
        # Split data cleanly into Historical and Projection subsets
        hist_df = final_filtered[final_filtered['category'] == 'Historical']
        proj_df = final_filtered[final_filtered['category'] != 'Historical']
        
        # 4. Render Dynamic Side-by-Side Visualizations Layout Grid Container Columns
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 📊 Historical Network Stations Installed")
            if not hist_df.empty:
                # Group charging stations by speed hardware type (Fast vs Slow network tracking vectors)
                chart_hist = hist_df.groupby(['year', 'powertrain'])['value'].sum().unstack(fill_value=0)
                st.line_chart(chart_hist)
            else:
                st.info("No historical observations recorded for this selection configuration.")
                
        with col2:
            st.markdown("### 🔮 Long-Term Infrastructure Projections")
            if not proj_df.empty:
                # Group prediction layers by scenario models running through 2035
                chart_proj = proj_df.groupby(['year', 'category'])['value'].sum().unstack(fill_value=0)
                st.line_chart(chart_proj)
            else:
                st.info("No projection infrastructure models recorded for this selection configuration.")
                
        # 5. Render Structured Ledger Record Table Matrix Underneath
        st.markdown("---")
        st.markdown("#### 📋 Consolidated Infrastructure Data Matrix")
        st.dataframe(final_filtered[['year', 'category', 'powertrain', 'unit', 'value']], use_container_width=True, hide_index=True)
        
    else:
        st.warning("⚠️ No recorded charging infrastructure entries found for this region selection.")

except Exception as e:
    st.error(f"Error executing infrastructure charging points engine: {e}")
