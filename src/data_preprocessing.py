"""
This script handles the data preprocessing steps such as loading, cleaning, 
and transforming raw data into a format suitable for machine learning models.
"""
import pandas as pd
import os

def load_and_preprocess_data(filepath):
    """
    Load data from a CSV file, extract time-based features, and print summary statistics.
    """
    if os.path.exists(filepath):
        # 1. Load the CSV file
        df = pd.read_csv(filepath)
        print(f"Data loaded successfully from {filepath}!\n")
        
        print("First 5 rows before preprocessing:")
        print(df.head())
        print("-" * 40)
        
        # 2. Print column names
        print("Columns in dataset:", df.columns.tolist())
        print("-" * 40)
        
        # 3. Convert 'date_time' column to datetime safely
        # We also handle errors if the column name differs slightly
        datetime_col = 'date_time'
        if datetime_col not in df.columns:
            # Fallback handling in case of slightly different column names
            possible_names = ['datetime', 'date', 'time', 'timestamp']
            for col in possible_names:
                if col in df.columns.str.lower():
                    # Pick the first matching column name
                    datetime_col = df.columns[df.columns.str.lower() == col][0]
                    break
                    
        if datetime_col in df.columns:
            try:
                # Convert the column to pandas datetime objects
                df[datetime_col] = pd.to_datetime(df[datetime_col])
                
                # 4. Create new features: hour, day, month, weekday
                df['hour'] = df[datetime_col].dt.hour
                df['day'] = df[datetime_col].dt.day
                df['month'] = df[datetime_col].dt.month
                df['weekday'] = df[datetime_col].dt.weekday
                
                print(f"Successfully formatted '{datetime_col}' to datetime.")
                print("New features added: hour, day, month, weekday.\n")
            except Exception as e:
                print(f"Error converting '{datetime_col}' to datetime: {e}\n")
        else:
            print("Warning: Could not find a datetime column to parse.\n")
            
        # Handle missing values by forward filling then backward filling
        print("Handling missing values...")
        df.ffill(inplace=True)
        df.bfill(inplace=True)
        print("Missing values handled.\n")
            
        # 5. Print first 5 rows after feature engineering
        print("First 5 rows after feature engineering:")
        print(df.head())
        print("-" * 40)
        
        # 6. Print missing values summary
        print("Missing values summary:")
        print(df.isnull().sum())
        print("-" * 40)
        
        return df
    else:
        print(f"Error: File not found at path '{filepath}'. Make sure traffic.csv is placed there.")
        return None

if __name__ == "__main__":
    # Resolve the absolute path of the data repository so it runs from anywhere
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    data_path = os.path.join(project_root, "data", "raw", "traffic.csv")
    
    # Run the data processing pipeline
    processed_df = load_and_preprocess_data(data_path)
