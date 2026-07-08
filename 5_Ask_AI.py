import streamlit as st
import pandas as pd
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from utils.llm_agent import query_dataframe

st.set_page_config(page_title="Ask AI", page_icon="🤖", layout="wide")

def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

st.markdown('<h2 class="highlight-text">5. LLM-Powered Query Answering</h2>', unsafe_allow_html=True)

if 'cleaned_data' not in st.session_state or st.session_state['cleaned_data'] is None:
    st.warning("Please clean your data in the 'Data Cleaning' section first.")
else:
    df = st.session_state['cleaned_data']
    
    st.markdown("### Talk to your Data")
    st.write("Use natural language to ask questions about your dataset. The AI will interpret your query and provide the answer.")
    
    api_key = st.text_input("Enter your OpenAI API Key:", type="password")
    
    query = st.text_input("Ask a question (e.g., 'What is the average sales?', 'Which category has the highest profit?')")
    
    if st.button("Generate Answer"):
        if not api_key:
            st.error("Please provide an API Key to use this feature.")
        elif not query:
            st.warning("Please enter a query.")
        else:
            with st.spinner("AI is analyzing your data..."):
                answer = query_dataframe(df, query, api_key)
                
                st.markdown("#### Answer:")
                st.info(answer)
                
    st.markdown("---")
    st.subheader("Data Reference")
    st.dataframe(df.head(5), use_container_width=True)
