import streamlit as st
import pandas as pd
import utils

# 1. Initialize Page View Settings
st.set_page_config(page_title="Data Explorer", page_icon="📊", layout="wide")

st.title("📊 Data Explorer")
st.markdown("Mode breakdown distributions for key EV parameters.")

try:
    # 2. Extract Data Source Matrix
    data = utils.load_clean_data()
    
    # 3. Sidebar Selection Blocks
    st.sidebar.header("Filter Explorer Matrix")
    
    # Select Country/Region
    all_countries = sorted([str(x) for x in data['region_country'].unique()])
    default_country_idx = all_countries.index('World') if 'World' in all_countries else 0
    selected_country = st.sidebar.selectbox("Select country / region", options=all_countries, index=default_country_idx)
    
    # Filter global dataset down to just this region to find valid matching years
    country_data = data[data['region_country'] == selected_country]
    
    # FIX: Dynamically populate year options ONLY if they exist for this specific region
    available_years = sorted(country_data['year'].unique(), reverse=True)
    if not available_years:
        available_years = [2022] # Safe default fallback
        
    selected_year = st.sidebar.selectbox("Select year", options=available_years)
    
    # 4. Filter parameters layout routing tabs
    params_of_interest = ["EV sales", "EV sales share", "EV charging points"]
    tab1, tab2, tab3 = st.tabs(params_of_interest)
    
    for tab, param in zip([tab1, tab2, tab3], params_of_interest):
        with tab:
            # Slicing for explicit parameter + country + year configuration context
            final_subset = country_data[(country_data['parameter'] == param) & (country_data['year'] == selected_year)]
            
            if not final_subset.empty:
                st.subheader(f"📊 {param} Distribution")
                
                # Check if we are handling charging points (where powertrain is the primary vector breakdown)
                if param == "EV charging points":
                    breakdown_col = "powertrain"
                    st.caption(f"Powertrain breakdown visualization for {selected_country} ({selected_year}):")
                else:
                    breakdown_col = "mode"
                    st.caption(f"Mode breakdown distributions for {selected_country} ({selected_year}):")
                
                # Prepare visual aggregation series metrics
                grouped_metrics = final_subset.groupby(breakdown_col)['value'].sum().reset_index()
                
                # Render Comparative Side-by-Side Interface Columns
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown(f"**Metrics Aggregated Chart Tracking**")
                    # Display clean bar chart visualization
                    st.bar_chart(data=grouped_metrics, x=breakdown_col, y="value", use_container_width=True)
                    
                with col2:
                    st.markdown("**Structured Summary Ledger Matrix**")
                    # Format column layout names cleanly before displaying
                    display_table = final_subset[[breakdown_col, 'unit', 'value', 'category']].copy()
                    st.dataframe(display_table, use_container_width=True, hide_index=True)
            else:
                # User-friendly dynamic warning notice
                st.info(f"ℹ️ No recorded entry rows found for **{param}** inside the dataset mapping for **{selected_country}** during the year **{selected_year}**.")

except Exception as e:
    st.error(f"Error executing visual data explorer pipeline module: {e}")
