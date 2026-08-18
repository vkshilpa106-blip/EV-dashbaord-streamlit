import streamlit as st
import pandas as pd

@st.cache_data
def load_data():
    """
    Unified performance data engine that safely reads the local Excel 
    dataset provided by the instructor, strips whitespaces from headings,
    and normalizes string metric rows to eliminate mixed-type sorting errors.
    """
    file_path = "data/EV data by country 2026.xlsx"
    data = pd.read_excel(file_path)
    
    # Clean accidental white space gaps in column labels
    data.columns = data.columns.str.strip()
    
    # Force absolute string conversions to protect drop-down components from mixed types
    text_columns = ['region_country', 'category', 'parameter', 'mode', 'powertrain', 'unit']
    for col in text_columns:
        if col in data.columns:
            data[col] = data[col].astype(str).str.strip()
            data[col] = data[col].replace({'nan': 'Unknown/Standard', '': 'Unknown/Standard'})
            data[col] = data[col].fillna('Unknown/Standard')
            
    return data
