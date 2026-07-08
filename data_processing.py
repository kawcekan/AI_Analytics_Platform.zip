import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder, StandardScaler

def clean_data(df, strategy='mean'):
    """
    Cleans the dataframe by handling missing values and duplicates.
    """
    # Create a copy to avoid SettingWithCopyWarning
    df_clean = df.copy()
    
    # Remove duplicates
    df_clean = df_clean.drop_duplicates()
    
    # Handle missing values
    for col in df_clean.columns:
        if df_clean[col].isnull().any():
            if df_clean[col].dtype == 'object':
                # Fill categorical with mode
                df_clean[col].fillna(df_clean[col].mode()[0], inplace=True)
            else:
                if strategy == 'mean':
                    df_clean[col].fillna(df_clean[col].mean(), inplace=True)
                elif strategy == 'median':
                    df_clean[col].fillna(df_clean[col].median(), inplace=True)
                else:
                    df_clean[col].fillna(0, inplace=True)
    return df_clean

def transform_data(df):
    """
    Prepares data for modeling (Encoding & Scaling).
    """
    df_transformed = df.copy()
    
    label_encoders = {}
    scaler = StandardScaler()
    
    # Identify numerical and categorical columns
    categorical_cols = df_transformed.select_dtypes(include=['object']).columns
    numerical_cols = df_transformed.select_dtypes(include=[np.number]).columns
    
    # Label encoding for categorical
    for col in categorical_cols:
        le = LabelEncoder()
        # Convert all to string first in case of mixed types
        df_transformed[col] = df_transformed[col].astype(str)
        df_transformed[col] = le.fit_transform(df_transformed[col])
        label_encoders[col] = le
        
    # Scaling numerical features
    if len(numerical_cols) > 0:
        df_transformed[numerical_cols] = scaler.fit_transform(df_transformed[numerical_cols])
        
    return df_transformed, label_encoders, scaler

def remove_outliers(df, columns):
    """
    Removes outliers using the IQR method.
    """
    df_out = df.copy()
    for col in columns:
        if pd.api.types.is_numeric_dtype(df_out[col]):
            Q1 = df_out[col].quantile(0.25)
            Q3 = df_out[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            df_out = df_out[(df_out[col] >= lower_bound) & (df_out[col] <= upper_bound)]
    return df_out
