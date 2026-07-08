import streamlit as st
import os

# Configure the main page
st.set_page_config(
    page_title="AI Analytics Platform",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load Custom CSS
def load_css(file_name):
    if os.path.exists(file_name):
        with open(file_name) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

load_css("assets/style.css")

def main():
    st.markdown('<h1 class="highlight-text" style="text-align: center; font-size: 3rem;">AI-Powered Analytics Engine</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #a0aec0;">Transform raw data into actionable insights instantly.</p>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### 🚀 Platform Features
        
        Our intelligent dashboard simplifies data science workflows into a seamless, automated experience:
        
        *   **Intelligent Data Upload:** Support for CSV and Excel files with automatic schema validation.
        *   **Automated Data Cleaning:** Smart imputation for missing values, outlier detection, and standardization.
        *   **Advanced Modeling:** Train Machine Learning (Random Forest) and Deep Learning (LSTM) models with zero code.
        *   **Interactive Visualization:** Auto-generated, interactive Plotly charts tailored to your dataset.
        *   **LLM Query Answering:** Talk to your data. Ask questions in natural language and get instant answers and visualizations.
        """)
        
    with col2:
        # A simple aesthetic placeholder block simulating a dashboard preview
        st.markdown("""
        <div style="background: rgba(255,255,255,0.05); padding: 20px; border-radius: 15px; border: 1px solid rgba(0,150,255,0.3); box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
            <h4 style="margin-top:0; color:#00b4db;">Platform Status</h4>
            <div style="display:flex; justify-content: space-between; margin-bottom: 10px;">
                <span>System Ready</span> <span style="color:#00ff88;">● Online</span>
            </div>
            <div style="display:flex; justify-content: space-between; margin-bottom: 10px;">
                <span>ML Compute Engine</span> <span style="color:#00ff88;">● Active</span>
            </div>
            <div style="display:flex; justify-content: space-between;">
                <span>LLM Gateway</span> <span style="color:#ffcc00;">● Awaiting Key</span>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    
    st.markdown("<h3 style='text-align: center;'>Get Started</h3>", unsafe_allow_html=True)
    
    # We provide a button to jump to the first page if possible, but Streamlit native 
    # multipage apps use the sidebar for navigation. We can use a hyperlink.
    st.markdown("""
    <div style="text-align: center; margin-top: 20px;">
        <p>Use the <b>sidebar navigation</b> to upload your dataset and begin the analysis pipeline.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
