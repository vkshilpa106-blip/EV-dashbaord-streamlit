import streamlit as st
import pandas as pd
import utils

# 1. Page Configuration Setup
st.set_page_config(
    page_title="Trends & Projections", 
    layout="wide"
)

st.title("📈 EV Market Historical Trends & 2035 Projections")
st.markdown("---")

try:
    # 2. Extract Data from Ingestion Engine
    data = utils.load_clean_data()
    
    # 3. Sidebar Configuration Setup
    st.sidebar.header("Filter Trend Analytics")
    
    # SYSTEM SAFETY SHIELD: Filter out any elements that aren't strings or are blank/NaN
    all_countries = sorted([
        str(x).strip() for x in data['region_country'].unique() 
        if pd.notna(x) and str(x).lower() != 'nan' and str(x).strip() != ''
    ])
    
    default_country_idx = all_countries.index('World') if 'World' in all_countries else 0
    selected_country = st.sidebar.selectbox("Select Country/Region", options=all_countries, index=default_country_idx)
    
    all_params = sorted([
        str(x).strip() for x in data['parameter'].unique() 
        if pd.notna(x) and str(x).lower() != 'nan' and str(x).strip() != ''
    ])
    
    default_param_idx = all_params.index('EV sales') if 'EV sales' in all_params else 0
    selected_param = st.sidebar.selectbox("Select Measurement Metric", options=all_params, index=default_param_idx)
    
    # Isolate relevant subset data to build dynamic secondary filters
    country_filtered = data[data['region_country'].astype(str) == selected_country]
    param_filtered = country_filtered[country_filtered['parameter'].astype(str) == selected_param]
    
    # Safety slice for vehicle modes list selection
    all_modes = sorted([
        str(x).strip() for x in param_filtered['mode'].unique() 
        if pd.notna(x) and str(x).lower() != 'nan' and str(x).strip() != ''
    ]) if not param_filtered.empty else ["All"]
    
    selected_mode = st.sidebar.selectbox("Select Vehicle Mode", options=all_modes)
    
    # 4. Final Dataset Slicing
    final_filtered = param_filtered[param_filtered['mode'].astype(str) == selected_mode]
    
    if not final_filtered.empty:
        st.subheader(f"📊 {selected_param} Timeline Profile for {selected_country} ({selected_mode})")
        
        # 5. Clean values data vector formats
        final_filtered['value'] = pd.to_numeric(final_filtered['value'], errors='coerce').fillna(0)
        final_filtered['year'] = pd.to_numeric(final_filtered['year'], errors='coerce').fillna(0).astype(int)
        
        # 6. Pivot Table Construction
        chart_data = final_filtered.groupby(['year', 'category'])['value'].sum().unstack(fill_value=0)
        
        # 7. Render interactive line chart visualization elements
        st.line_chart(chart_data)
        
        # 8. Render Data Table Ledger Matrix Underneath
        st.markdown("#### 📋 Aggregated Data Ledger Matrix")
        st.dataframe(final_filtered[['year', 'category', 'powertrain', 'unit', 'value']], use_container_width=True, hide_index=True)
        
    else:
        st.warning("⚠️ No comparative visual observations found for the selected configurations. Try adjusting your sidebar filter choices.")

except Exception as e:
    st.error(f"Error executing manual trends visualization engine: {e}")
