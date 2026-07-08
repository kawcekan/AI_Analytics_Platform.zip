import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Upload Data", page_icon="📁", layout="wide")

# Load Custom CSS
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

st.markdown('<h2 class="highlight-text">1. Data Upload</h2>', unsafe_allow_html=True)
st.write("Upload your dataset to begin. We accept CSV, XLSX, and Excel files.")

uploaded_file = st.file_uploader("Drop your file here", type=["csv", "xlsx", "xls"])

if uploaded_file is not None:
    try:
        # Determine file type and load
        if uploaded_file.name.endswith('.csv'):
            df = pd.read_csv(uploaded_file)
        else:
            df = pd.read_excel(uploaded_file)
            
        st.success(f"File '{uploaded_file.name}' successfully loaded!")
        
        # Save to session state for use in other pages
        st.session_state['raw_data'] = df
        st.session_state['cleaned_data'] = None # Reset downstream data
        
        # Display dataset preview
        st.subheader("Data Preview")
        st.dataframe(df.head(10), use_container_width=True)
        
        # Display some quick stats
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Rows", df.shape[0])
        with col2:
            st.metric("Total Columns", df.shape[1])
        with col3:
            missing_vals = df.isnull().sum().sum()
            st.metric("Missing Values", missing_vals)
            
    except Exception as e:
        st.error(f"Error loading file: {e}")
else:
    if 'raw_data' in st.session_state:
        st.info("A dataset is already loaded in memory.")
        if st.button("Clear Dataset"):
            for key in ['raw_data', 'cleaned_data', 'transformed_data']:
                if key in st.session_state:
                    del st.session_state[key]
            st.rerun()
