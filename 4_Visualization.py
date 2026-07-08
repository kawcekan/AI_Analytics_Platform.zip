import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Visualization", page_icon="📈", layout="wide")

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

st.markdown('<h2 class="highlight-text">4. Automated Visualization</h2>', unsafe_allow_html=True)

if 'cleaned_data' not in st.session_state or st.session_state['cleaned_data'] is None:
    st.warning("Please clean your data in the 'Data Cleaning' section first.")
else:
    df = st.session_state['cleaned_data']
    
    col1, col2 = st.columns([1, 3])
    
    with col1:
        st.subheader("Chart Controls")
        chart_type = st.selectbox("Select Chart Type", ["Scatter Plot", "Line Chart", "Bar Chart", "Histogram", "Heatmap (Correlation)"])
        
        if chart_type != "Heatmap (Correlation)":
            x_axis = st.selectbox("X-Axis", df.columns.tolist())
            y_axis = st.selectbox("Y-Axis", df.columns.tolist()[::-1])
            color_by = st.selectbox("Color By (Optional)", ["None"] + df.columns.tolist())
        
    with col2:
        st.subheader("Interactive Dashboard")
        
        try:
            if chart_type == "Scatter Plot":
                fig = px.scatter(df, x=x_axis, y=y_axis, color=None if color_by == "None" else color_by, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Line Chart":
                fig = px.line(df, x=x_axis, y=y_axis, color=None if color_by == "None" else color_by, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Bar Chart":
                fig = px.bar(df, x=x_axis, y=y_axis, color=None if color_by == "None" else color_by, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Histogram":
                fig = px.histogram(df, x=x_axis, color=None if color_by == "None" else color_by, template="plotly_dark")
                st.plotly_chart(fig, use_container_width=True)
                
            elif chart_type == "Heatmap (Correlation)":
                numeric_df = df.select_dtypes(include=['float64', 'int64'])
                if numeric_df.empty:
                    st.error("No numeric columns available for correlation heatmap.")
                else:
                    corr = numeric_df.corr()
                    fig = px.imshow(corr, text_auto=True, template="plotly_dark", color_continuous_scale="RdBu_r")
                    st.plotly_chart(fig, use_container_width=True)
                    
        except Exception as e:
            st.error(f"Could not generate chart: {e}")
