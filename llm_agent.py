import pandas as pd
from pandasai import SmartDataframe
from pandasai.llm import OpenAI

def query_dataframe(df, query, api_key):
    """
    Query the dataframe using natural language via PandasAI.
    """
    try:
        # Initialize the LLM
        # Using OpenAI as default. We can support Gemini or others if needed.
        llm = OpenAI(api_token=api_key)
        
        # Create a SmartDataframe
        sdf = SmartDataframe(df, config={"llm": llm})
        
        # Execute query
        response = sdf.chat(query)
        
        return response
    except Exception as e:
        return f"Error processing query: {str(e)}"
