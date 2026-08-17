import streamlit as st
import pandas as pd

@st.cache_data
def load_clean_data():
    """
    Optimized data engine that safely reads the raw EV Excel dataset,
    strips whitespace from column headings, and strictly forces string 
    conversions on text columns to eliminate mixed-type sorting errors.
    """
    file_path = "data/EV data by country 2026.xlsx"
    data = pd.read_excel(file_path)
    
    # 1. Clean accidental white space gaps in column labels
    data.columns = data.columns.str.strip()
    
    # 2. Strict type casting to prevent 'str' vs 'float' errors
    text_columns = ['region_country', 'category', 'parameter', 'mode', 'powertrain', 'unit', 'Aggregate group']
    for col in text_columns:
        if col in data.columns:
            data[col] = data[col].astype(str).str.strip()
            # Replace empty or raw nan text markers with a clean fallback string
            data[col] = data[col].replace({'nan': 'Unknown/Standard', '': 'Unknown/Standard'})
            data[col] = data[col].fillna('Unknown/Standard')
            
    return data
