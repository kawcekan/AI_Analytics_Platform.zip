import streamlit as st
import pandas as pd
import os
import sys

# Ensure utils can be imported
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.data_processing import clean_data, remove_outliers

st.set_page_config(page_title="Data Cleaning", page_icon="🧹", layout="wide")

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

st.markdown('<h2 class="highlight-text">2. Data Cleaning & Preprocessing</h2>', unsafe_allow_html=True)

if 'raw_data' not in st.session_state:
    st.warning("Please upload a dataset in the 'Upload Data' section first.")
else:
    df = st.session_state['raw_data']
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("Cleaning Options")
        
        imputation_strategy = st.selectbox(
            "Missing Value Imputation (Numerical)",
            ["mean", "median", "zero"]
        )
        
        handle_outliers = st.checkbox("Remove Outliers (IQR Method)", value=True)
        outlier_cols = []
        if handle_outliers:
            numeric_cols = df.select_dtypes(include=['float64', 'int64']).columns.tolist()
            outlier_cols = st.multiselect("Select columns to remove outliers from", numeric_cols, default=numeric_cols[:2] if len(numeric_cols) > 0 else [])
            
        if st.button("Apply Cleaning"):
            with st.spinner("Cleaning data..."):
                # Clean Data
                cleaned_df = clean_data(df, strategy=imputation_strategy)
                
                # Remove Outliers
                if handle_outliers and len(outlier_cols) > 0:
                    cleaned_df = remove_outliers(cleaned_df, outlier_cols)
                
                st.session_state['cleaned_data'] = cleaned_df
                st.success("Data cleaned successfully!")
                
    with col2:
        if 'cleaned_data' in st.session_state:
            st.subheader("Cleaned Dataset Preview")
            st.dataframe(st.session_state['cleaned_data'].head(10), use_container_width=True)
            
            # Show comparison
            st.markdown("### 📊 Dataset Changes")
            c1, c2, c3 = st.columns(3)
            with c1:
                st.metric("Original Rows", df.shape[0])
                st.metric("New Rows", st.session_state['cleaned_data'].shape[0])
            with c2:
                orig_missing = df.isnull().sum().sum()
                st.metric("Original Missing Values", orig_missing)
                new_missing = st.session_state['cleaned_data'].isnull().sum().sum()
                st.metric("New Missing Values", new_missing)
            with c3:
                # Provide download button
                csv = st.session_state['cleaned_data'].to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Cleaned Data",
                    data=csv,
                    file_name='cleaned_dataset.csv',
                    mime='text/csv',
                )
        else:
            st.info("Configure options and click 'Apply Cleaning' to see results.")
