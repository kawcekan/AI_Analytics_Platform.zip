import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.data_processing import transform_data
from utils.modeling import train_classification_model, train_regression_model, train_clustering_model, train_lstm_model

st.set_page_config(page_title="Analytics & Modeling", page_icon="⚙️", layout="wide")

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

st.markdown('<h2 class="highlight-text">3. Predictive Modeling</h2>', unsafe_allow_html=True)

if 'cleaned_data' not in st.session_state or st.session_state['cleaned_data'] is None:
    st.warning("Please clean your data in the 'Data Cleaning' section first.")
else:
    df = st.session_state['cleaned_data']
    
    st.markdown("### Data Transformation")
    if st.button("Transform Data (Encode & Scale)"):
        with st.spinner("Transforming data..."):
            transformed_df, encoders, scaler = transform_data(df)
            st.session_state['transformed_data'] = transformed_df
            st.success("Data successfully transformed and ready for modeling!")
            
    if 'transformed_data' in st.session_state:
        st.markdown("---")
        st.markdown("### Machine Learning Studio")
        
        t_df = st.session_state['transformed_data']
        
        col1, col2 = st.columns([1, 2])
        
        with col1:
            problem_type = st.selectbox("Select Problem Type", ["Classification", "Regression", "Clustering", "Time Series (LSTM)"])
            
            target_col = None
            if problem_type in ["Classification", "Regression", "Time Series (LSTM)"]:
                target_col = st.selectbox("Select Target Variable", t_df.columns.tolist())
                
            model_type = "Random Forest"
            if problem_type == "Classification":
                model_type = st.selectbox("Select Model", ["Random Forest", "Logistic Regression"])
            elif problem_type == "Regression":
                model_type = st.selectbox("Select Model", ["Random Forest", "Linear Regression"])
            elif problem_type == "Clustering":
                n_clusters = st.slider("Number of Clusters (K)", 2, 10, 3)
            elif problem_type == "Time Series (LSTM)":
                time_steps = st.slider("Time Steps (Lag)", 1, 30, 10)
                epochs = st.slider("Epochs", 5, 50, 10)
                
            train_btn = st.button("🚀 Train Model")
            
        with col2:
            if train_btn:
                with st.spinner("Training model... This might take a moment."):
                    try:
                        if problem_type == "Classification":
                            model, metric, preds = train_classification_model(t_df, target_col, model_type)
                            st.success(f"Model Trained! Accuracy: {metric:.2f}")
                            st.session_state['predictions'] = preds
                            
                        elif problem_type == "Regression":
                            model, metric, preds = train_regression_model(t_df, target_col, model_type)
                            st.success(f"Model Trained! Mean Squared Error: {metric:.2f}")
                            st.session_state['predictions'] = preds
                            
                        elif problem_type == "Clustering":
                            model, clusters = train_clustering_model(t_df, n_clusters)
                            st.success("Clustering Completed!")
                            st.session_state['predictions'] = clusters
                            
                        elif problem_type == "Time Series (LSTM)":
                            res = train_lstm_model(t_df, target_col, time_steps, epochs)
                            if res[0] is None:
                                st.error(res[1])
                            else:
                                model, metric, preds = res
                                st.success(f"LSTM Trained! Mean Squared Error: {metric:.2f}")
                                st.session_state['predictions'] = preds
                                
                    except Exception as e:
                        st.error(f"Error during training: {e}")
                        
        if 'predictions' in st.session_state:
            st.markdown("#### Predictions Preview")
            st.write(st.session_state['predictions'][:10]) # Show first 10 predictions
